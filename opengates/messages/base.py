from abc import ABC

from pydantic import BaseModel, ConfigDict

from opengates.messages.content import BaseMessageContent
from opengates.messages.content.text import TextMessageContent

__all__ = [
    "BaseMessage",
]


class BaseMessage(BaseModel, ABC):
    model_config = ConfigDict(extra="forbid")
    role: str
    content: list[BaseMessageContent]

    def __init__(
        self,
        role: str,
        content: list[BaseMessageContent] | BaseMessageContent | str,
    ):
        super().__init__(role=role, content=self._format_content(content))

    def _format_content(
        self,
        content: list[BaseMessageContent] | BaseMessageContent | str,
    ) -> list[BaseMessageContent]:
        if isinstance(content, str):
            return [TextMessageContent(text=content)]
        elif isinstance(content, BaseMessageContent):
            return [content]
        elif isinstance(content, list):
            return content
        else:
            raise ValueError("Invalid content format")
