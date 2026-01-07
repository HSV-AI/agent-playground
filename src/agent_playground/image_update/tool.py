import os
from typing import Optional
from pydantic_ai import Tool, BinaryImage
from pydantic_ai.messages import BinaryContent, ToolReturn
from openai import OpenAI
import base64
import re

from pathlib import Path
debug = True

# NOTE - I had to move the update image method out of the ImageUpdateTool class
#       to avoid getting a JSON Serializable error.

async def update_image(prompt: str, image_url: str) -> ToolReturn:
    """This tool updates an image based on the provided prompt and image URL."""

    if debug:
        image_path = Path("output_image.png")
        image_bytes = image_path.read_bytes()
        print(f"Loaded image from {image_path}, size: {len(image_bytes)} bytes")
        return ToolReturn(
            return_value="Image successfully updated and attached.",
            content = [BinaryImage(data=image_bytes, media_type="image/png")]
        )

    print(f"Sending request to Gemini 3 Pro to: {prompt}...")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ.get("OPENROUTER_API_KEY", "sk-or-..."),
        default_headers={
            "HTTP-Referer": "https://your-app-url.com",
            "X-Title": "My Image Editor",
        }
    )

    try:
        completion = client.chat.completions.create(
            model="google/gemini-3-pro-image-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": prompt
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": image_url
                            }
                        }
                    ]
                }
            ],
            modalities=["text", "image"],
        )

        # Extracting the Image
        raw_response = completion.model_dump()
        message_data = raw_response['choices'][0]['message']

        if 'images' in message_data and message_data['images']:
            image_info = message_data['images'][0]['image_url']

            if 'url' in image_info:
                image_url = image_info['url']
                print("\n--- Success! Image Returned ---")
                print(f"Image URL: {image_url[:50]}... (truncated)")

                match = re.match(r"data:(?P<type>.+?);base64,(?P<data>.+)", image_url)
                if not match:
                    raise ValueError("Invalid Data URL format")

                media_type = match.group("type")
                encoded_data = match.group("data")

                image_bytes = base64.b64decode(encoded_data)

                return ToolReturn(
                    return_value="Image successfully updated and attached.",
                    content=[BinaryContent(data=image_bytes, media_type=media_type)]
                )

        print("\n--- No Content or Image Found ---")
        print("Full raw dump for debugging:", message_data)

    except Exception as e:
        print(f"An error occurred: {e}")
        raise

class ImageUpdateTool:
    """Standalone class for managing the image update tool."""

    def as_pydantic_tool(self) -> Tool:
        return Tool(
                    function=update_image,
                    takes_ctx=False,
                    description=f"This tool updates an image based on the provided prompt and image URL.",
                    name="update_image_tool",
                    max_retries=1,
                )
    
