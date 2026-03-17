from opengates.guardrails.base import BaseGuardrail

__all__ = [
    "ForbiddenTermsGuardrail",
]


class ForbiddenTermsGuardrail(BaseGuardrail):
    forbidden_terms: list[str]

    def apply(
        self,
        input: str,
    ):
        for term in self.forbidden_terms:
            if term in input:
                raise ValueError(f"Input contains forbidden term: {term}")
