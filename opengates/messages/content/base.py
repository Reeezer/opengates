from abc import ABC

from pydantic import BaseModel, ConfigDict

__all__ = [
    "BaseMessageContent",
]


class BaseMessageContent(BaseModel, ABC):
    model_config = ConfigDict(extra="forbid")
    type: str
