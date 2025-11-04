import os
import asyncio
from pydantic_ai import Agent, DocumentUrl, ImageUrl
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openrouter import OpenRouterProvider
from datetime import datetime
import logfire
from .types import User

# --- Configuration ---
# Since OpenRouter has a unified API, we can use the OpenAIChatModel with a custom provider.
OPENROUTER_MODEL = "openai/gpt-4o-mini"  # Using a placeholder compatible Gemma model

class Runner:

    def __init__(self):
        self._model = OpenAIChatModel(
            OPENROUTER_MODEL,
            provider=OpenRouterProvider(
                api_key=os.environ.get("OPENROUTER_API_KEY") 
            ),
        )

        self._agent = Agent(
            model=self._model,
        )  

        @self._agent.tool_plain
        def get_current_time() -> datetime:
            return datetime.now()

        @self._agent.tool_plain
        def get_user() -> User:
            return User(name='John', age=30)

        @self._agent.tool_plain
        def get_company_logo() -> ImageUrl:
            return ImageUrl(url='https://iili.io/3Hs4FMg.png')

        @self._agent.tool_plain
        def get_document() -> DocumentUrl:
            return DocumentUrl(url='https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf')

    def run(self, prompt: str):
        return self._agent.run(prompt)
    
    def run_sync(self, prompt: str):
        return self._agent.run_sync(prompt)

async def main():

    # configure logfire
    LOGFIRE_TOKEN = os.environ.get('LOGFIRE_TOKEN')
    if LOGFIRE_TOKEN:
      logfire.configure(token=LOGFIRE_TOKEN)
      logfire.instrument_pydantic_ai()

    agent = Runner()
    result = await agent.run('What time is it?')
    print(result.output)
    #> The current time is 10:45 PM on April 17, 2025.

    result = await agent.run('What is the user name?')
    print(result.output)
    #> The user's name is John.

    result = await agent.run('What is the company name in the logo?')
    print(result.output)
    #> The company name in the logo is "Pydantic."

    result = await agent.run('What is the main content of the document?')
    print(result.output)
    #> The document contains just the text "Dummy PDF file."

if __name__ == '__main__':
    asyncio.run(main())