import os
import asyncio
from typing import Any
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openrouter import OpenRouterProvider
from pydantic_ai.mcp import load_mcp_servers
import logfire

from pathlib import Path

OPENROUTER_MODEL = "openai/gpt-4o-mini"  # Using a placeholder compatible Gemma model

class FileSystemAgent():
    """Agent specialized for file system operations using the FileSystem MCP tool."""
    
    def __init__(self):

        CONFIG_FILE_PATH = Path(__file__).parent / "mcp_config.json"
        SYSTEM_PROMPT_FILE_PATH = Path(__file__).parent / "system_prompt.md"

        # 1. Configure the LLM for OpenRouter
        # We use OpenAIModel because OpenRouter is OpenAI-compatible
        # and we pass the OpenRouterProvider to configure the endpoint.
        self._model = OpenAIChatModel(
            OPENROUTER_MODEL,
            provider=OpenRouterProvider(
                api_key=os.environ.get("OPENROUTER_API_KEY") 
            ),
        )

        self._toolsets = load_mcp_servers(str(CONFIG_FILE_PATH))
        self._system_prompt_text = SYSTEM_PROMPT_FILE_PATH.read_text(encoding='utf-8')
        
        self._agent = Agent(
            model=self._model,  # Use a powerful model capable of tool use/reasoning
            toolsets=self._toolsets,
            system_prompt=self._system_prompt_text,
        )

    def run(self, prompt: str) -> Any:
        return self._agent.run(prompt)
    
    def run_sync(self, prompt: str) -> Any:
        return self._agent.run_sync(prompt)

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
    print("Starting File System Agent Runner...\n")
    asyncio.run(main())
