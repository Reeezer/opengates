import dotenv

from opengates.ai_gateway.pipeline.guardrails import (
    ForbiddenTermsGuardrail,
    GuardrailAction,
    PIIGuardrail,
)
from opengates.messages import UserMessage
from opengates.models.completion import GoogleCompletion

if __name__ == "__main__":
    dotenv.load_dotenv()
    guardrails = [
        PIIGuardrail(),
        ForbiddenTermsGuardrail(
            forbidden_terms=["forbidden"],
            output_action=GuardrailAction.WARN,
        ),
    ]
    llm = GoogleCompletion(guardrails=guardrails)
    history = UserMessage(content="What is the capital of France? forbidden")
    response = llm.generate(history)
    print(response)
