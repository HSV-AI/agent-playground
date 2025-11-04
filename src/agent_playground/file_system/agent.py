import os
import asyncio
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openrouter import OpenRouterProvider
from pydantic_ai.mcp import load_mcp_servers
import logfire

from pathlib import Path

class FileSystemAgent(Agent):
    """Agent specialized for file system operations using the FileSystem MCP tool."""
    def __init__(self, **kwargs):
        CONFIG_FILE_PATH = Path(__file__).parent / "mcp_config.json"
        SYSTEM_PROMPT_FILE_PATH = Path(__file__).parent / "system_prompt.md"

        OPENROUTER_MODEL = "openai/gpt-4o-mini"  # Using a placeholder compatible Gemma model

        # 1. Configure the LLM for OpenRouter
        # We use OpenAIModel because OpenRouter is OpenAI-compatible
        # and we pass the OpenRouterProvider to configure the endpoint.
        openrouter_model = OpenAIModel(
            OPENROUTER_MODEL,
            provider=OpenRouterProvider(
                api_key=os.environ.get("OPENROUTER_API_KEY") 
            ),
        )

        mcp_toolsets = load_mcp_servers(str(CONFIG_FILE_PATH))
        system_prompt_text = SYSTEM_PROMPT_FILE_PATH.read_text(encoding='utf-8')
        super().__init__(
            model=openrouter_model,  # Use a powerful model capable of tool use/reasoning
            toolsets=mcp_toolsets,
            system_prompt=system_prompt_text,
        )


async def main():

    # configure logfire
    LOGFIRE_TOKEN = os.environ.get('LOGFIRE_TOKEN')
    if LOGFIRE_TOKEN:
      logfire.configure(token=LOGFIRE_TOKEN)
      logfire.instrument_pydantic_ai()

    USER_PROMPT_FILE_PATH = Path(__file__).parent / "user_prompt.md"
    user_prompt_text = USER_PROMPT_FILE_PATH.read_text(encoding='utf-8')

    print(f"Running Agent Task: {user_prompt_text}\n")

    agent = FileSystemAgent()
    
    # Run the agent, specifying the desired output structure
    result = await agent.run(
        user_prompt_text,
    )

    print("Task Complete! Check agent output for results.")
    print(result)

if __name__ == '__main__':
    asyncio.run(main())
