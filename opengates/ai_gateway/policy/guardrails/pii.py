import re

from opengates.ai_gateway.policy.guardrails.base import BaseGuardrail, GuardrailAction

__all__ = [
    "PIIGuardrail",
]

PII_PATTERNS: dict[str, re.Pattern[str]] = {
    "email": re.compile(r"\b[a-zA-Z0-9._%+\-]+@[a-zA-Z0-9.\-]+\.[a-zA-Z]{2,}\b"),
    "phone": re.compile(
        r"\b(?:\+?\d{1,3}[-.\s]?)?(?:\(?\d{2,4}\)?[-.\s]?)\d{3,4}[-.\s]?\d{3,4}\b"
    ),
    "ipv4": re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b"),
    "ssn_us": re.compile(r"\b\d{3}-\d{2}-\d{4}\b"),
    "credit_card_like": re.compile(r"\b(?:\d[ -]*?){13,19}\b"),
}


class PIIGuardrail(BaseGuardrail):
    in_input: bool = True
    in_output: bool = True

    def apply(
        self,
        input: str,
    ) -> GuardrailAction:
        # FIXME Placeholder implementation for PII detection
        # In a real implementation, this would use a machine learning model
        # or a more comprehensive set of regex patterns to detect PII.
        for _, pattern in PII_PATTERNS.items():
            if pattern.search(input):
                return self.output_action
        return GuardrailAction.ALLOW
