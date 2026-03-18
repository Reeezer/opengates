from opengates.ai_gateway.context import RequestContext
from opengates.ai_gateway.policy.resolved_policy import ResolvedPolicy
from opengates.ai_gateway.policy.resolver.base import BasePolicyResolver

__all__ = [
    "InMemoryPolicyResolver",
]


class InMemoryPolicyResolver(BasePolicyResolver):
    def __init__(
        self,
        global_policy: ResolvedPolicy,
        group_policies: dict[str, ResolvedPolicy] | None = None,
        project_policies: dict[str, ResolvedPolicy] | None = None,
        user_policies: dict[str, ResolvedPolicy] | None = None,
    ):
        self.global_policy = global_policy
        self.group_policies = group_policies or {}
        self.project_policies = project_policies or {}
        self.user_policies = user_policies or {}

    def resolve(
        self,
        context: RequestContext,
    ) -> ResolvedPolicy:
        # Start with global policy
        policy = self.global_policy

        # Override with group policy if exists
        if context.group_id and context.group_id in self.group_policies:
            policy = self.group_policies[context.group_id]

        # Override with project policy if exists
        if context.project_id and context.project_id in self.project_policies:
            policy = self.project_policies[context.project_id]

        # Override with user policy if exists
        if context.user_id and context.user_id in self.user_policies:
            policy = self.user_policies[context.user_id]

        return policy
