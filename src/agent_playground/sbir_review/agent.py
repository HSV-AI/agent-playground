import os
import asyncio
from pydantic_ai import Agent, AgentRunResult
from pydantic_ai.mcp import MCPServerStdio
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openrouter import OpenRouterProvider
from pydantic_ai.mcp import load_mcp_servers
import logfire
from typing import Any
from types import CoroutineType

from agent_playground.sbir_review.models import Topic, ScrapeResult

from pathlib import Path

class SBIRAgent():
    """Agent specialized for scraping SBIR topics using BrowserAutomation tools."""
    def __init__(self, **kwargs):
        CONFIG_FILE_PATH = Path(__file__).parent / "mcp_config.json"
        SYSTEM_PROMPT_FILE_PATH = Path(__file__).parent / "system_prompt.md"

        OPENROUTER_MODEL = "openai/gpt-4o-mini"  # Using a placeholder compatible Gemma model

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
            output_type=ScrapeResult,
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
    logfire.configure(token=LOGFIRE_TOKEN)
    logfire.instrument_pydantic_ai()

    USER_PROMPT_FILE_PATH = Path(__file__).parent / "user_prompt.md"
    user_prompt_text = USER_PROMPT_FILE_PATH.read_text(encoding='utf-8')

    print(f"Running Agent Task: {user_prompt_text}\n")

    agent = SBIRAgent()
    
    # Run the agent, specifying the desired output structure
    result = await agent.run(
        user_prompt_text,
    )

    print("Task Complete! Extracted Structured Data:")
    for topic in result.output.topics:
        print(topic)

if __name__ == '__main__':
    asyncio.run(main())
