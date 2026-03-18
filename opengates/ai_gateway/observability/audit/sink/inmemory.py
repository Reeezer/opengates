from threading import Lock

from opengates.ai_gateway.observability.audit.event import AuditEvent
from opengates.ai_gateway.observability.audit.sink.base import BaseAuditSink

__all__ = [
    "InMemoryAuditSink",
]


class InMemoryAuditSink(BaseAuditSink):
    def __init__(
        self,
    ) -> None:
        self.events: list[AuditEvent] = []
        self.lock = Lock()

    def write(
        self,
        event: AuditEvent,
    ) -> None:
        with self.lock:
            self.events.append(event)

    def read(
        self,
    ) -> list[AuditEvent]:
        with self.lock:
            return self.events.copy()

    def flush(
        self,
    ) -> None:
        with self.lock:
            self.events.clear()
