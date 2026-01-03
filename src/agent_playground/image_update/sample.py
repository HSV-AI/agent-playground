import os
from openai import OpenAI
import base64
from pydantic_ai.messages import BinaryContent
import re

# 1. Setup your OpenRouter API Key
# You can set this in your environment variables or replace directly below (not recommended for sharing)
OPENROUTER_API_KEY = os.environ.get("OPENROUTER_API_KEY", "sk-or-...") 
YOUR_SITE_URL = "https://your-app-url.com"  # Optional: for OpenRouter rankings
YOUR_SITE_NAME = "My Image Editor"          # Optional: for OpenRouter rankings

def change_image_text(instruction):
    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=OPENROUTER_API_KEY,
        default_headers={
            "HTTP-Referer": YOUR_SITE_URL,
            "X-Title": YOUR_SITE_NAME,
        }
    )

    print(f"Sending request to Gemini 3 Pro to: {instruction}...")

    try:
        completion = client.chat.completions.create(
            model="google/gemini-3-pro-image-preview",
            messages=[
                {
                    "role": "user",
                    "content": [
                        {
                            "type": "text",
                            "text": instruction
                        },
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": "https://hsv.ai/wp-content/uploads/2025/02/Paper-Review.png"
                            }
                        }
                    ]
                }
            ],
            modalities=["text", "image"],
            # Google's Gemini models often require explicit "modality" flags 
            # or simply infer based on content. OpenRouter standardizes this.
        )

        # 2. Extracting the Image
        # The standard client.choices[0].message.content is often empty.
        # We must look at the raw dictionary to find the custom 'images' field.
        raw_response = completion.model_dump()
        message_data = raw_response['choices'][0]['message']

        # Check for image in the proprietary 'images' field
        if 'images' in message_data and message_data['images']:
            image_info = message_data['images'][0]['image_url']
            
            # It usually returns a Data URL (base64)
            if 'url' in image_info:
                image_url = image_info['url']
                print("\n--- Success! Image Returned ---")
                print(f"Image URL: {image_url[:50]}... (truncated)")
                
                # Regex to match: data:[media_type];base64,[data]
                match = re.match(r"data:(?P<type>.+?);base64,(?P<data>.+)", image_url)
                if not match:
                    raise ValueError("Invalid Data URL format")

                media_type = match.group("type")  # e.g., 'image/png'
                encoded_data = match.group("data")
                
                # Decode the base64 string into raw bytes
                image_bytes = base64.b64decode(encoded_data)
                
                with open("output_image.png", "wb") as f:
                    f.write(image_bytes)

                return BinaryContent(data=image_bytes, media_type=media_type)

            else:
                print("Image field found but no URL present.")
                print(image_info)
        
        # Fallback: Sometimes it IS in the content, so check that too
        elif message_data.get('content'):
            print("\n--- Text Response ---")
            print(message_data['content'])
        
        else:
            print("\n--- No Content or Image Found ---")
            print("Full raw dump for debugging:", message_data)

    except Exception as e:
        print(f"An error occurred: {e}")
        return None

# --- Configuration ---

# 2. Instruction to change text
# Be specific about what text to remove and what to add.
PROMPT = 'Replace the text "Paper Review" in the image with "Image Updated!" and return the updated image.'

# --- Run ---
if __name__ == "__main__":
    change_image_text(PROMPT)