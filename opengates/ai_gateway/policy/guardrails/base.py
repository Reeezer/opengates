from abc import ABC, abstractmethod
from enum import Enum

from pydantic import BaseModel, ConfigDict

__all__ = [
    "BaseGuardrail",
    "GuardrailAction",
]


class GuardrailAction(str, Enum):
    BLOCK = "block"
    WARN = "warn"
    ALLOW = "allow"


class BaseGuardrail(BaseModel, ABC):
    model_config = ConfigDict(extra="forbid")
    in_input: bool
    in_output: bool
    output_action: GuardrailAction = GuardrailAction.BLOCK

    @abstractmethod
    def apply(
        self,
        input: str,
    ) -> GuardrailAction:
        raise NotImplementedError
