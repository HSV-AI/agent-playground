import os
import asyncio
from pydantic_ai import Agent
from pydantic_ai.mcp import MCPServerStreamableHTTP
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openrouter import OpenRouterProvider
import logfire

from .types import GitHubIssueReport, GitHubIssue
from pathlib import Path

class GitHubIssuesAgent():
    """Agent specialized for interacting with GitHub repositories to manage issues."""
    def __init__(self):
        CONFIG_FILE_PATH = Path(__file__).parent / "mcp_config.json"
        SYSTEM_PROMPT_FILE_PATH = Path(__file__).parent / "system_prompt.md"

        OPENROUTER_MODEL = "openai/gpt-4o-mini" # Example model, adjust as needed

        self._model = OpenAIChatModel(
            OPENROUTER_MODEL,
            provider=OpenRouterProvider(
                api_key=os.environ.get("OPENROUTER_API_KEY")
            ),
        )
        
        # Using this approach instead of load_mcp_servers to directly define the MCP server
        # because I could not find a way to pass the environment variable through the config file.
        self._toolsets = [
            MCPServerStreamableHTTP("https://api.githubcopilot.com/mcp",
                headers={"Authorization": f"Bearer {os.environ.get("GITHUB_TOKEN")}"})
        ]

        self._system_prompt_text = SYSTEM_PROMPT_FILE_PATH.read_text(encoding='utf-8')
        
        super().__init__(
            model=self._model,
            toolsets=self._toolsets,
            output_type=GitHubIssueReport,
            system_prompt=self._system_prompt_text,
        )

    def run(self, prompt: str):
        return self._agent.run(prompt)
    
    def run_sync(self, prompt: str):
        return self._agent.run_sync(prompt)
    
async def main():

    LOGFIRE_TOKEN = os.environ.get('LOGFIRE_TOKEN')
    logfire.configure(token=LOGFIRE_TOKEN)
    logfire.instrument_pydantic_ai()

    USER_PROMPT_FILE_PATH = Path(__file__).parent / "user_prompt.md"
    user_prompt_text = USER_PROMPT_FILE_PATH.read_text(encoding='utf-8')

    print(f"Running Agent Task: {user_prompt_text}\n")

    agent = GitHubIssuesAgent()

    # Run the agent, specifying the desired output structure
    result = await agent.run(
        user_prompt_text,
        output_type=GitHubIssueReport,
    )

    print("Task Complete! GitHub Issue Report:")
    # print(result.output)
    print(f"Repository: {result.output.owner}/{result.output.repository}")
    print(f"Summary: {result.output.report_summary}")
    for i, issue in enumerate(result.output.issues):
        print(f"Issue {i+1}:")
        print(f"  Title: {issue.title}")
        print(f"  URL: {issue.url}")
        print(f"  State: {issue.state}")
        print(f"  Updated At: {issue.updated_at}")
        print(f"  Labels: {', '.join(issue.labels)}")
        print(f"  Author: {issue.author}")
    if result.output.error_message:
        print(f"Error: {result.output.error_message}")


if __name__ == '__main__':
    asyncio.run(main())
