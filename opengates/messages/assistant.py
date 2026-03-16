from opengates.messages.base import BaseMessage
from opengates.messages.content.base import BaseMessageContent

__all__ = [
    "AssistantMessage",
]


class AssistantMessage(BaseMessage):
    def __init__(self, content: list[BaseMessageContent] | BaseMessageContent | str):
        super().__init__(role="assistant", content=content)
