from sqlmodel import SQLModel, Field
from typing import Optional
from datetime import datetime


class Counter(SQLModel, table=True):
    """Model to store counter state"""

    __tablename__ = "counters"  # type: ignore[assignment]

    id: Optional[int] = Field(default=None, primary_key=True)
    value: int = Field(default=0)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)


# Non-persistent schema for counter operations
class CounterUpdate(SQLModel, table=False):
    """Schema for counter update operations"""

    value: int
