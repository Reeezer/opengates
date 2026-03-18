from datetime import UTC, datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

from opengates.ai_gateway.context import RequestContext

__all__ = [
    "AuditEvent",
]


class AuditEvent(BaseModel):
    model_config = ConfigDict(extra="forbid")
    timestamp: datetime = Field(default_factory=lambda: datetime.now(UTC))
    request_context: RequestContext
    model_name: str
    payload: dict[str, Any]
