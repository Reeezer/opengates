from abc import ABC, abstractmethod

from opengates.ai_gateway.context import RequestContext
from opengates.ai_gateway.policy.resolved_policy import ResolvedPolicy

__all__ = [
    "BasePolicyResolver",
]


class BasePolicyResolver(ABC):
    @abstractmethod
    def resolve(
        self,
        context: RequestContext,
    ) -> ResolvedPolicy:
        raise NotImplementedError
