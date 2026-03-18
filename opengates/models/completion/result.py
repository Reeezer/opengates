from pydantic import BaseModel, ConfigDict

__all__ = [
    "CompletionResult",
]


class CompletionResult(BaseModel):
    model_config = ConfigDict(extra="forbid")
    text: str
    input_tokens: int
    output_tokens: int
