from uuid import UUID
from pydantic import BaseModel


class CreateSecretMessageRequest(BaseModel):
    place_id: UUID
    content: str
