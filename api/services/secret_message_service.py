from uuid import UUID

from fastapi import HTTPException

from api.db.models.secret_messages import SecretMessageModel
from api.db.models.users import User
from api.repository.place_repository import PlaceRepository
from api.repository.secret_message_repository import SecretMessageRepository
from api.web.api.secret_messages.request.create_secret_message_request import CreateSecretMessageRequest
from api.web.api.secret_messages.request.get_secret_message_request import GetSecretMessageRequest


class SecretMessageService:
    def __init__(self, repository: SecretMessageRepository, place_repository: PlaceRepository):
        self.secret_message_repository = repository
        self.place_repository = place_repository

    async def create_secret_message(self, user: User, request: CreateSecretMessageRequest):

        await self._validate_place_exists(request.place_id)

        secret_message = SecretMessageModel(place_id=request.place_id, author_id=user.id, content=request.content)
        return await self.secret_message_repository.save(secret_message)


    async def get_message(self, user: User, request: GetSecretMessageRequest):

        await self._validate_place_exists(request.place_id)

        secret_message = await self.secret_message_repository.find_by_place_id_ordered_by_created_date(request.place_id)

        return secret_message


    async def _validate_place_exists(self, place_id: UUID):

        place = await self.place_repository.find_by_id(place_id)

        if not place:
            raise HTTPException(status_code=404, detail="place not found")




