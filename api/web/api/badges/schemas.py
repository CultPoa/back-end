from uuid import UUID
from typing import List
from pydantic import BaseModel


class BadgeUnlockRequest(BaseModel):
    placeId: UUID


class BadgeItem(BaseModel):
    id: str
    name: str
    description: str
    unlocked: bool
    progress: int
    goal: int


class BadgeListResponse(BaseModel):
    total: int
    unlocked: int
    badges: List[BadgeItem]
