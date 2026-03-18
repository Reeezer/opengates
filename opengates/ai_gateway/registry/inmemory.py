from typing import Any

from opengates.ai_gateway.registry.base import BaseModelRegistry, CompletionFactory
from opengates.models.completion import BaseCompletion

__all__ = [
    "InMemoryModelRegistry",
]


class InMemoryModelRegistry(BaseModelRegistry):
    def __init__(
        self,
    ) -> None:
        self._registry: dict[str, CompletionFactory] = {}

    def register(
        self,
        model_name: str,
        factory: CompletionFactory,
    ) -> None:
        if model_name in self._registry:
            raise ValueError(f"Model {model_name} is already registered")
        self._registry[model_name] = factory

    def get(
        self,
        model_name: str,
    ) -> BaseCompletion[Any]:
        if model_name not in self._registry:
            raise ValueError(f"Model {model_name} is not registered")
        factory = self._registry[model_name]
        return factory()

    def list_models(self) -> list[str]:
        return list(self._registry.keys())
