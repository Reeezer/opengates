import os

from pydantic import BaseModel

from opengates.messages.assistant import BaseMessage
from opengates.messages.user import UserMessage

__all__ = [
    "BaseCompletion",
]


class BaseCompletion(BaseModel):
    api_key: str
    model_name: str
    client: object | None = None

    def __init__(self, api_key_env_var: str, model_name: str):
        api_key = os.getenv(api_key_env_var)
        super().__init__(api_key=api_key, model_name=model_name)

    def generate(
        self,
        history: list[BaseMessage] | BaseMessage | str,
    ) -> str:
        raise NotImplementedError

    def _format_history(self, history: list[BaseMessage] | BaseMessage | str) -> list[dict]:
        history_list: list[BaseMessage]
        if isinstance(history, str):
            history_list = [UserMessage(content=history)]
        elif isinstance(history, BaseMessage):
            history_list = [history]
        elif isinstance(history, list):
            history_list = [msg for msg in history]
        else:
            raise ValueError("Invalid history format")

        return [msg.model_dump_json(exclude_none=True, serialize_as_any=True) for msg in history_list]
