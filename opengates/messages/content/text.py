from typing import Literal

from opengates.messages.content.base import BaseMessageContent

__all__ = [
    "TextMessageContent",
]


class TextMessageContent(BaseMessageContent):
    type: Literal["text"] = "text"
    text: str