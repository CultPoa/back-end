from uuid import UUID
from pydantic import BaseModel


class GetSecretMessageRequest(BaseModel):
    place_id: UUID
