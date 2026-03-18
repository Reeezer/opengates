from opengates.ai_gateway.pipeline.guardrails.base import BaseGuardrail, GuardrailAction

__all__ = [
    "ForbiddenTermsGuardrail",
]


class ForbiddenTermsGuardrail(BaseGuardrail):
    forbidden_terms: list[str]
    in_input: bool = True
    in_output: bool = True

    def apply(
        self,
        input: str,
    ) -> GuardrailAction:
        for term in self.forbidden_terms:
            if term in input:
                return self.output_action
        return GuardrailAction.ALLOW
