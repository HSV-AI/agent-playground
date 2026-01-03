import os
import asyncio
from pydantic_ai import Agent, ImageUrl
from pydantic_ai.mcp import MCPServerStreamableHTTP
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openrouter import OpenRouterProvider
import logfire
from typing import Any

from pathlib import Path

class ImageUpdateAgent():
    """Agent specialized for interacting with GitHub repositories to manage issues."""
    def __init__(self):
        SYSTEM_PROMPT_FILE_PATH = Path(__file__).parent / "system_prompt.md"

        OPENROUTER_MODEL = "google/gemini-3-pro-image-preview" # Example model, adjust as needed

        self._model = OpenAIChatModel(
            OPENROUTER_MODEL,
            provider=OpenRouterProvider(
                api_key=os.environ.get("OPENROUTER_API_KEY")
            ),
        )
        
        self._system_prompt_text = SYSTEM_PROMPT_FILE_PATH.read_text(encoding='utf-8')
        
        self._agent = Agent(
            model=self._model,
            # system_prompt=self._system_prompt_text,
        )

    def run(self, prompt: str) -> Any:
        return self._agent.run( [
            prompt,
            ImageUrl(url="https://hsv.ai/wp-content/uploads/2025/02/Paper-Review.png")
        ])
    
    def run_sync(self, prompt: str) -> Any:
        return self._agent.run_sync([
            prompt,
            ImageUrl(url="https://hsv.ai/wp-content/uploads/2025/02/Paper-Review.png")
        ])
    
async def main():

    LOGFIRE_TOKEN = os.environ.get('LOGFIRE_TOKEN')
    logfire.configure(token=LOGFIRE_TOKEN)
    logfire.instrument_pydantic_ai()

    print(f"Running Agent Task\n")

    agent = ImageUpdateAgent()

    # Run the agent, specifying the desired output structure
    result = await agent.run(
        'Replace the text "Paper Review" in the image with "Image Updated!" and return the updated image. When generating an image, you MUST also output the text "IMAGE_GENERATED" so that the system knows the generation is complete.'
    )

    # Now we can safely extract the binary image from the message history
    # The image is usually in the last message's parts
    for message in reversed(result.new_messages()):
        if hasattr(message, 'parts'):
            for part in message.parts:
                # Check for binary content (attributes vary slightly by SDK version)
                # We look for 'content' (bytes) or specific part kinds
                if hasattr(part, 'content') and isinstance(part.content, bytes):
                    print(f"Found image! Size: {len(part.content)} bytes")
                    
                    # Save the image
                    Path("output_cityscape.png").write_bytes(part.content)
                    break
                
                # Some versions wrap it in inline_data
                if hasattr(part, 'inline_data') and part.inline_data:
                    print("Found inline image data!")
                    Path("output_cityscape.png").write_bytes(part.inline_data.data)
                    break

    print(result.output)


if __name__ == '__main__':
    asyncio.run(main())
