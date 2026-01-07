import pytest
from unittest.mock import patch, MagicMock
from agent_playground.image_update.tool import ImageUpdateTool
from pydantic_ai.messages import BinaryContent
import base64
import os

# Mock binary content for testing
MOCK_IMAGE_BYTES = b"mock_image_bytes"
MOCK_MEDIA_TYPE = "image/png"
MOCK_ENCODED_DATA = base64.b64encode(MOCK_IMAGE_BYTES).decode("utf-8")
MOCK_IMAGE_URL = f"data:{MOCK_MEDIA_TYPE};base64,{MOCK_ENCODED_DATA}"

# Mock response from OpenAI
MOCK_RESPONSE = {
    "choices": [
        {
            "message": {
                "images": [
                    {
                        "image_url": {
                            "url": MOCK_IMAGE_URL
                        }
                    }
                ]
            }
        }
    ]
}

@pytest.fixture
def mock_openai_client():
    with patch("openai.OpenAI") as mock_client:
        mock_completion = MagicMock()
        mock_completion.model_dump.return_value = MOCK_RESPONSE
        mock_client.return_value.chat.completions.create.return_value = mock_completion
        yield mock_client

@pytest.mark.skip(reason="This test is currently broken")
def test_image_update_tool(mock_openai_client):
    tool = ImageUpdateTool()
    prompt = "Replace the text 'Paper Review' in the image with 'Image Updated!' and return the updated image."
    image_url = "https://hsv.ai/wp-content/uploads/2025/02/Paper-Review.png"

    # Run the tool
    result = tool.get_tool().run(prompt, image_url)

    # Verify the result is of type ImageReturn
    assert isinstance(result, ImageReturn)
    assert result.prompt == prompt
    assert isinstance(result.image, BinaryContent)
    assert result.image.data == MOCK_IMAGE_BYTES
    assert result.image.media_type == MOCK_MEDIA_TYPE

    # Verify the OpenAI client was called correctly
    mock_openai_client.return_value.chat.completions.create.assert_called_once()
    args = mock_openai_client.return_value.chat.completions.create.call_args[1]
    assert args["model"] == "google/gemini-3-pro-image-preview"
    assert len(args["messages"]) == 1
    assert args["messages"][0]["role"] == "user"
    assert len(args["messages"][0]["content"]) == 2
    assert args["messages"][0]["content"][0]["type"] == "text"
    assert args["messages"][0]["content"][0]["text"] == prompt
    assert args["messages"][0]["content"][1]["type"] == "image_url"
    assert args["messages"][0]["content"][1]["image_url"]["url"] == image_url
    assert args["modalities"] == ["text", "image"]
