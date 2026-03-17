import logging
import os
import sys

import tenacity
from pydantic import BaseModel

from opengates.messages.assistant import BaseMessage
from opengates.messages.user import UserMessage

__all__ = [
    "BaseCompletion",
]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

MULTIPLIER = 1
MIN_WAIT = 1
MAX_WAIT = 60
STOP_AFTER_ATTEMPT = 5


class BaseCompletion(BaseModel):
    api_key: str
    model_name: str
    client: object | None = None

    def __init__(self, api_key_env_var: str, model_name: str):
        api_key = os.getenv(api_key_env_var)
        super().__init__(api_key=api_key, model_name=model_name)

    @tenacity.retry(
        wait=tenacity.wait_exponential(multiplier=MULTIPLIER, min=MIN_WAIT, max=MAX_WAIT),
        stop=tenacity.stop_after_attempt(max_attempt_number=STOP_AFTER_ATTEMPT),
        reraise=(ValueError,),
        before=tenacity.before_log(logger, logging.INFO),
    )
    def generate(self, history: list[BaseMessage] | BaseMessage | str) -> str:
        return self._generate_logic(history)

    def _generate_logic(self, history: list[BaseMessage] | BaseMessage | str) -> str:
        raise NotImplementedError

    def _format_history(self, history: list[BaseMessage] | BaseMessage | str) -> list[dict]:
        history_list: list[BaseMessage]
        if isinstance(history, str):
            history_list = [UserMessage(content=history)]
        elif isinstance(history, BaseMessage):
            history_list = [history]
        elif isinstance(history, list):
            history_list = history
        else:
            raise ValueError("Invalid history format")

        return [msg.model_dump_json(exclude_none=True, serialize_as_any=True) for msg in history_list]
