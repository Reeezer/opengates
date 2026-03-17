from opengates.guardrails.base import BaseGuardrail

__all__ = [
    "PIIDetectionGuardrail",
]

PII_TERMS = ["name", "email", "phone", "address"]


class PIIDetectionGuardrail(BaseGuardrail):
    def apply(
        self,
        input: str,
    ):
        # FIXME Placeholder implementation for PII detection
        # In a real implementation, this would use a more sophisticated method
        # to detect PII, such as regex patterns or a machine learning model.
        for term in PII_TERMS:
            if term in input.lower():
                raise ValueError(f"Input contains potential PII term: {term}")
        return input
