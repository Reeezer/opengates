from abc import ABC, abstractmethod

from opengates.ai_gateway.observability.audit.event import AuditEvent

__all__ = [
    "BaseAuditSink",
]


class BaseAuditSink(ABC):
    @abstractmethod
    def write(
        self,
        event: AuditEvent,
    ) -> None:
        raise NotImplementedError

    @abstractmethod
    def read(
        self,
    ) -> list[AuditEvent]:
        raise NotImplementedError

    @abstractmethod
    def flush(
        self,
    ) -> None:
        raise NotImplementedError
