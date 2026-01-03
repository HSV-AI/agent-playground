from pydantic import BaseModel
from pydantic_ai.messages import BinaryContent

class ImageReturn(BaseModel):
    prompt: str
    image: BinaryContent
