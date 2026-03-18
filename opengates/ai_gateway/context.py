from pydantic import BaseModel, ConfigDict


class RequestContext(BaseModel):
    model_config = ConfigDict(extra="forbid")
    request_id: str
    user_id: str
    group_id: str | None = None
    project_id: str | None = None
