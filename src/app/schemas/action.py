from datetime import datetime
from typing import List, Dict, Any, Optional

from pydantic import BaseModel, field_validator, Field


class ActionProposal(BaseModel):
    """
    Intermediate action proposal (before saving/execution).
    """
    id: str
    title: str
    tools: List[str] = Field(
        examples=["email, chat, todos"],
        description="Tools to execute. Choose one of the tools which fits the needs of the proposed action.")
    description: str = Field(description="Human-readable description of the proposed action.")
    executed_at: Optional[datetime] = None
    payload: Dict[str,Any] = Field(description="Payload for the used tools")
    requires_approval: bool = Field(default=True, description="Whether or not to require human approval.")
    confidence: float
    created_at: datetime = datetime.now()

    @field_validator("tools")
    @classmethod
    def normalize_tools(cls, v):
        if isinstance(v, str):
            return [t.strip() for t in v.split(",") if t.strip()]
        if isinstance(v, list):
            return [str(t).lower() for t in v]
        raise ValueError("tools must be list[str] or comma-separated string")
