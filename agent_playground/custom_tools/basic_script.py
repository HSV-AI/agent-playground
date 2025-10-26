import os
from pydantic_ai import Agent, DocumentUrl, ImageUrl
from pydantic_ai.models.openai import OpenAIModel
from pydantic_ai.providers.openrouter import OpenRouterProvider
from datetime import datetime
from pydantic import BaseModel

class User(BaseModel):
    name: str
    age: int

# --- Configuration ---
# Since OpenRouter has a unified API, we can use the OpenAIModel with a custom provider.
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

# 2. Create the Agent with the WebSearchTool
agent = Agent(
    model=openrouter_model,
)

@agent.tool_plain
def get_current_time() -> datetime:
    return datetime.now()

@agent.tool_plain
def get_user() -> User:
    return User(name='John', age=30)

@agent.tool_plain
def get_company_logo() -> ImageUrl:
    return ImageUrl(url='https://iili.io/3Hs4FMg.png')

@agent.tool_plain
def get_document() -> DocumentUrl:
    return DocumentUrl(url='https://www.w3.org/WAI/ER/tests/xhtml/testfiles/resources/pdf/dummy.pdf')

result = agent.run_sync('What time is it?')
print(result.output)
#> The current time is 10:45 PM on April 17, 2025.

result = agent.run_sync('What is the user name?')
print(result.output)
#> The user's name is John.

result = agent.run_sync('What is the company name in the logo?')
print(result.output)
#> The company name in the logo is "Pydantic."

result = agent.run_sync('What is the main content of the document?')
print(result.output)
#> The document contains just the text "Dummy PDF file."