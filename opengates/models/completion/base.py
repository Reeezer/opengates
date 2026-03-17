import logging
import os
from abc import abstractmethod
from typing import Generic, TypeVar

import tenacity
from pydantic import BaseModel, ConfigDict, PrivateAttr

from opengates.ai_gateway.guardrails import BaseGuardrail
from opengates.messages import BaseMessage, TextMessageContent, UserMessage

__all__ = [
    "BaseCompletion",
]

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

MULTIPLIER = 1
MIN_WAIT = 1
MAX_WAIT = 60
STOP_AFTER_ATTEMPT = 5

ClientT = TypeVar("ClientT")


class BaseCompletion(BaseModel, Generic[ClientT]):
    model_config = ConfigDict(extra="forbid")
    api_key: str
    model_name: str
    guardrails: list[BaseGuardrail]

    _client: ClientT | None = PrivateAttr(default=None)

    def __init__(
        self,
        api_key_env_var: str,
        model_name: str,
        guardrails: list[BaseGuardrail] | None = None,
    ):
        api_key = os.getenv(api_key_env_var)
        if not api_key:
            raise ValueError(
                f"API key not found in environment variable: {api_key_env_var}"
            )
        super().__init__(
            api_key=api_key,
            model_name=model_name,
            guardrails=guardrails or [],
        )

    @property
    def client(self) -> ClientT:
        if self._client is None:
            self._client = self._initialize_client()
        return self._client

    @abstractmethod
    def _initialize_client(self) -> ClientT:
        raise NotImplementedError

    @tenacity.retry(
        wait=tenacity.wait_exponential(
            multiplier=MULTIPLIER, min=MIN_WAIT, max=MAX_WAIT
        ),
        stop=tenacity.stop_after_attempt(max_attempt_number=STOP_AFTER_ATTEMPT),
        retry=tenacity.retry_if_exception_type((TimeoutError, ConnectionError)),
        before=tenacity.before_log(logger, logging.INFO),
    )
    def generate(
        self,
        history: list[BaseMessage] | BaseMessage | str,
    ) -> str:
        # Format history
        history_list = self._format_history(history)

        # Apply input guardrails
        for guardrail in self.guardrails:
            if guardrail.in_input:
                for msg in history_list:
                    for content in msg.content:
                        if isinstance(content, TextMessageContent):
                            guardrail.apply(content.text)

        # Generate response
        history_raw = self._history_to_raw(history_list)
        response = self._generate_logic(history_raw)

        # Apply output guardrails
        for guardrail in self.guardrails:
            if guardrail.in_output:
                response = guardrail.apply(response)

        return response

    @abstractmethod
    def _generate_logic(
        self,
        history_raw: list[dict],
    ) -> str:
        raise NotImplementedError

    def _format_history(
        self,
        history: list[BaseMessage] | BaseMessage | str,
    ) -> list[BaseMessage]:
        if isinstance(history, str):
            return [UserMessage(content=history)]
        elif isinstance(history, BaseMessage):
            return [history]
        elif isinstance(history, list):
            return history
        else:
            raise ValueError("Invalid history format")

    def _history_to_raw(self, history_list: list[BaseMessage]) -> list[dict]:
        return [
            msg.model_dump_json(exclude_none=True, serialize_as_any=True)
            for msg in history_list
        ]
