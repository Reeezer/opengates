from opengates.messages.content.base import BaseMessageContent

__all__ = [
    "ImageMessageContent",
]


class ImageMessageContent(BaseMessageContent):
    type: str = "text"
    image_url: str
