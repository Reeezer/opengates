from abc import ABC

from pydantic import BaseModel, ConfigDict

__all__ = [
    "BaseGuardrail",
]


class BaseGuardrail(BaseModel, ABC):
    model_config = ConfigDict(extra="forbid")
    in_input: bool
    in_output: bool

    def apply(
        self,
        input: str,
    ):
        raise NotImplementedError
