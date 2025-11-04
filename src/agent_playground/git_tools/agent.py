import os
import asyncio
from pydantic_ai import Agent
from pydantic_ai.mcp import load_mcp_servers
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openrouter import OpenRouterProvider

from .types import MergeRequestSuggestion
import logfire

from pathlib import Path

class GitToolsAgent(Agent):
    """Agent specialized for interacting with Git repositories and suggesting merge requests."""
    def __init__(self, **kwargs):
        CONFIG_FILE_PATH = Path(__file__).parent / "mcp_config.json"
        SYSTEM_PROMPT_FILE_PATH = Path(__file__).parent / "system_prompt.md"

        OPENROUTER_MODEL = "openai/gpt-4o-mini" # Example model, adjust as needed

        openrouter_model = OpenAIModel(
            OPENROUTER_MODEL,
            provider=OpenRouterProvider(
                api_key=os.environ.get("OPENROUTER_API_KEY")
            ),
        )

        mcp_toolsets = load_mcp_servers(str(CONFIG_FILE_PATH))
        system_prompt_text = SYSTEM_PROMPT_FILE_PATH.read_text(encoding='utf-8')
        super().__init__(
            model=openrouter_model,
            # output_type=MergeRequestSuggestion,
            toolsets=mcp_toolsets,
            system_prompt=system_prompt_text,
        )


async def main():

    LOGFIRE_TOKEN = os.environ.get('LOGFIRE_TOKEN')
    logfire.configure(token=LOGFIRE_TOKEN)
    logfire.instrument_pydantic_ai()

    USER_PROMPT_FILE_PATH = Path(__file__).parent / "user_prompt.md"
    user_prompt_text = USER_PROMPT_FILE_PATH.read_text(encoding='utf-8')

    print(f"Running Agent Task: {user_prompt_text}\n")

    agent = GitToolsAgent()

    # Run the agent, specifying the desired output structure
    result = await agent.run(
        user_prompt_text,
    )

    print("Task Complete! Suggested Merge Request:")
    print(result.output)
    # print(f"Title: {result.output.title}")
    # print(f"Description: {result.output.description}")
    # print(f"Reviewers: {result.output.suggested_reviewers}")
    # print(f"Diff Summary: {result.output.diff_summary.summary_message}")
    # if result.output.error_message:
    #     print(f"Error: {result.output.error_message}")


if __name__ == '__main__':
    asyncio.run(main())
