import dotenv

from opengates.ai_gateway.guardrails import (
    ForbiddenTermsGuardrail,
    PIIGuardrail,
)
from opengates.messages import UserMessage
from opengates.models.completion import GoogleCompletion

if __name__ == "__main__":
    dotenv.load_dotenv()
    guardrails = [
        PIIGuardrail(),
        ForbiddenTermsGuardrail(forbidden_terms=["forbidden"]),
    ]
    llm = GoogleCompletion(guardrails=guardrails)
    history = UserMessage(content="What is the capital of France? forbidde")
    response = llm.generate(history)
    print(response)
