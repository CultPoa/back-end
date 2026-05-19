from uuid import UUID
from pydantic import BaseModel


class BadgeUnlockRequest(BaseModel):
    placeId: UUID
