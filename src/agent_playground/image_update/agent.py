import os
import re
import asyncio
import base64
from pydantic_ai import Agent, BinaryImage
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openrouter import OpenRouterProvider
import logfire
from typing import Any

from pathlib import Path
from agent_playground.image_update.tool import ImageUpdateTool

class ImageUpdateAgent():
    """Agent specialized for updating text in images using OpenAI's Gemini model."""

    def __init__(self):
        SYSTEM_PROMPT_FILE_PATH = Path(__file__).parent / "system_prompt.md"

        OPENROUTER_MODEL = "openai/gpt-4o-mini" # Example model, adjust as needed
        # OPENROUTER_MODEL = "mistralai/devstral-2512"
        self._model = OpenAIChatModel(
            OPENROUTER_MODEL,
            provider=OpenRouterProvider(
                api_key=os.environ.get("OPENROUTER_API_KEY")
            ),
        )

        self._tool = ImageUpdateTool()
        pydantic_tool = self._tool.as_pydantic_tool()

        self._system_prompt_text = SYSTEM_PROMPT_FILE_PATH.read_text(encoding='utf-8')

        self._agent = Agent(
            model=self._model,
            system_prompt=self._system_prompt_text,
            tools = [pydantic_tool],
            output_type=BinaryImage,
        )


    def run(self, prompt: str) -> Any:
        return self._agent.run(prompt)

    def run_sync(self, prompt: str) -> Any:
        return self._agent.run(prompt)
    
async def main():

    LOGFIRE_TOKEN = os.environ.get('LOGFIRE_TOKEN')
    logfire.configure(token=LOGFIRE_TOKEN)
    logfire.instrument_pydantic_ai()

    print(f"Running Agent Task\n")

    agent = ImageUpdateAgent()

    prompt = """
            Replace the text "Paper Review" in the image with "Image Updated!" and return the updated image. 
            The url of the image to edit is: https://hsv.ai/wp-content/uploads/2025/02/Paper-Review.png
        """
    
    # Run the agent, specifying the desired output structure
    result = await agent.run(
        prompt=prompt
    )

    # Extract the image from the result
    image_return = result.output

    print(result.output)
    print(f"Lenght of image data: {len(image_return.data)} bytes")
    image_url = image_return.data_uri
    print("\n--- Success! Image Returned ---")
    print(f"Image URL: {image_url[:50]}... (truncated)")

    match = re.match(r"data:(?P<type>.+?);base64,(?P<data>.+)", image_url)
    if not match:
        # Try using the data bytes directly
        with open("agent_output_image.png", "wb") as f:
            f.write(image_return.data)

    else:
        media_type = match.group("type")
        encoded_data = match.group("data")
        print(f"Lenth of encoded data: {len(encoded_data)}")
        image_bytes = base64.b64decode(encoded_data)

        with open("agent_output_image.png", "wb") as f:
            f.write(image_bytes)



if __name__ == '__main__':
    asyncio.run(main())
