from logging import getLogger

from pydantic import BaseModel, ConfigDict

from opengates.ai_gateway.policy.guardrails import BaseGuardrail
from opengates.ai_gateway.policy.guardrails.base import GuardrailAction

__all__ = [
    "ResolvedPolicy",
]

logger = getLogger(__name__)


class ResolvedPolicy(BaseModel):
    model_config = ConfigDict(extra="forbid")
    allowed_models: list[str]
    guardrails: list[BaseGuardrail]

    _input_guardrails: list[BaseGuardrail] | None = None
    _output_guardrails: list[BaseGuardrail] | None = None

    @property
    def input_guardrails(
        self,
    ) -> list[BaseGuardrail]:
        if self._input_guardrails is None:
            self._input_guardrails = [g for g in self.guardrails if g.in_input]
        return self._input_guardrails

    @property
    def output_guardrails(
        self,
    ) -> list[BaseGuardrail]:
        if self._output_guardrails is None:
            self._output_guardrails = [g for g in self.guardrails if g.in_output]
        return self._output_guardrails

    def validate_model_access(
        self,
        model_name: str,
    ) -> bool:
        return model_name in self.allowed_models

    def apply_input_guardrails(
        self,
        text: str,
    ) -> None:
        self._apply_guardrails(
            guardrails=self.input_guardrails,
            text=text,
        )

    def apply_output_guardrails(
        self,
        text: str,
    ) -> None:
        self._apply_guardrails(
            guardrails=self.output_guardrails,
            text=text,
        )

    def _apply_guardrails(
        self,
        guardrails: list[BaseGuardrail],
        text: str,
    ) -> None:
        for guardrail in guardrails:
            action = guardrail.apply(input=text)

            if action == GuardrailAction.BLOCK:
                raise ValueError(
                    f"Text blocked by guardrail: {guardrail.__class__.__name__}"
                )
            elif action == GuardrailAction.WARN:
                logger.warning(
                    f"Text warning from guardrail {guardrail.__class__.__name__}: {text}"
                )
