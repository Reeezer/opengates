from pydantic import BaseModel, ConfigDict


class AIGateway(BaseModel):
    model_config = ConfigDict(extra="forbid")
