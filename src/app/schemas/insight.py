from typing import Optional, List
from uuid import uuid4

from pydantic import Field, field_validator, BaseModel


class Evidence(BaseModel):
    source: Optional[str] = None
    page: Optional[int] = None
    file_chunk_id: int
    page_chunk_id: int


class Insight(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid4()))
    title: str
    summary: str
    confidence: float
    evidence: List[Evidence] = []

    @field_validator("confidence")
    @classmethod
    def clamp_confidence(cls, v):
        if v is None:
            return 0.0
        if v < 0:
            return 0.0
        if v > 1:
            return 1.0
        return float(v)