from opengates.ai_gateway.policy.guardrails.base import BaseGuardrail, GuardrailAction

__all__ = [
    "ToxicityGuardrail",
]

TOXICITY_TERMS = [
    "hate",
    "violence",
    "abuse",
    "discrimination",
    "harassment",
    "racism",
    "sexism",
    "homophobia",
    "transphobia",
    "xenophobia",
    "slur",
    "offensive",
    "insult",
    "threat",
    "bully",
    "idiot",
    "stupid",
    "dumb",
    "fool",
    "moron",
    "bastard",
    "asshole",
    "bitch",
    "dick",
    "pussy",
]


class ToxicityGuardrail(BaseGuardrail):
    in_input: bool = True
    in_output: bool = True

    def apply(
        self,
        input: str,
    ) -> GuardrailAction:
        # FIXME Placeholder implementation for toxicity detection
        # In a real implementation, this would use a machine learning model
        # or a more comprehensive list of terms and context-aware analysis to detect toxicity.
        for term in TOXICITY_TERMS:
            if term in input.lower():
                return self.output_action
        return GuardrailAction.ALLOW
