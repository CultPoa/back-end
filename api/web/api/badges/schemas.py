from uuid import UUID
from pydantic import BaseModel


class BadgeUnlockRequest(BaseModel):
    placeId: UUID

class BadgeListResponse(BaseModel):
    total: int
    unlocked: int
    badges: list
