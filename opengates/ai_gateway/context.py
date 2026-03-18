from pydantic import BaseModel, ConfigDict

__all__ = [
    "RequestContext",
]


class RequestContext(BaseModel):
    model_config = ConfigDict(extra="forbid")
    request_id: str
    group_id: str | None = None
    project_id: str | None = None
    user_id: str
