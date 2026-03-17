import dotenv

from opengates.ai_gateway.guardrails import (
    ForbiddenTermsGuardrail,
    PIIDetectionGuardrail,
)
from opengates.messages import UserMessage
from opengates.models.completion import GoogleCompletion

if __name__ == "__main__":
    dotenv.load_dotenv()
    guardrails = [
        PIIDetectionGuardrail(),
        ForbiddenTermsGuardrail(forbidden_terms=["forbidden"]),
    ]
    llm = GoogleCompletion(guardrails=guardrails)
    history = UserMessage(content="What is the capital of France? forbidden")
    response = llm.generate(history)
    print(response)
