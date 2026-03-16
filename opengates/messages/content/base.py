from abc import ABC

from pydantic import BaseModel, ConfigDict

__all__ = [
    "BaseMessageContent",
]


class BaseMessageContent(BaseModel, ABC):
    type: str

    model_config = ConfigDict(extra="forbid")
