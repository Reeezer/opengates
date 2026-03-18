import dotenv

from opengates.ai_gateway.context import RequestContext
from opengates.ai_gateway.gateway import AIGateway
from opengates.ai_gateway.policy.guardrails import (
    ForbiddenTermsGuardrail,
    GuardrailAction,
    PIIGuardrail,
)
from opengates.ai_gateway.policy.resolved_policy import ResolvedPolicy
from opengates.ai_gateway.policy.resolver.inmemory import InMemoryPolicyResolver
from opengates.ai_gateway.registry.inmemory import InMemoryModelRegistry
from opengates.models.completion import GoogleCompletion

if __name__ == "__main__":
    dotenv.load_dotenv()

    # Build model registry
    registry = InMemoryModelRegistry()
    registry.register(
        model_name="google-lite",
        factory=lambda: GoogleCompletion(model_name="gemini-2.5-flash-lite"),
    )

    # Build policy (with guardrails)
    policy = ResolvedPolicy(
        allowed_models=["google-lite"],
        guardrails=[
            PIIGuardrail(),
            ForbiddenTermsGuardrail(
                forbidden_terms=["forbidden"],
                output_action=GuardrailAction.WARN,
            ),
        ],
    )
    resolver = InMemoryPolicyResolver(global_policy=policy)

    # Build AI Gateway
    gateway = AIGateway(
        model_registry=registry,
        policy_resolver=resolver,
    )

    # Request context + call
    context = RequestContext(
        request_id="req-123",
        user_id="user-123",
        group_id="group-123",
        project_id="project-123",
    )
    response = gateway.generate(
        context=context,
        model_name="google-lite",
        history="What is the capital of France? forbidden",
    )
    print(response)
