from abc import ABC, abstractmethod
from typing import Any, Callable

from opengates.models.completion import BaseCompletion

__all__ = [
    "BaseModelRegistry",
    "CompletionFactory",
]

CompletionFactory = Callable[[], BaseCompletion[Any]]


class BaseModelRegistry(ABC):
    @abstractmethod
    def register(
        self,
        model_name: str,
        factory: CompletionFactory,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def get(
        self,
        model_name: str,
    ) -> BaseCompletion[Any]:
        raise NotImplementedError

    @abstractmethod
    def list_models(
        self,
    ) -> list[str]:
        raise NotImplementedError
