from typing import List

from pydantic import BaseModel, Field


# Data models
class User(BaseModel):
    tg_id: int
    name: str
    ready_status: bool = False
    clubs: List[str] = Field(default_factory=list)
