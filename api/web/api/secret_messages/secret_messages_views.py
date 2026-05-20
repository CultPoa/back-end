from typing import Annotated

from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.db.dependencies import get_db_session
from api.db.models.users import User, current_active_user
from api.repository.place_repository import PlaceRepository
from api.repository.secret_message_repository import SecretMessageRepository
from api.services.secret_message_service import SecretMessageService
from api.web.api.secret_messages.request.create_secret_message_request import CreateSecretMessageRequest
from api.web.api.secret_messages.request.get_secret_message_request import GetSecretMessageRequest

router = APIRouter(prefix="/secret-message")

def get_service(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> SecretMessageService:
    return SecretMessageService(SecretMessageRepository(session), PlaceRepository(session))


@router.post(path="", status_code=status.HTTP_201_CREATED)
async def create_secret_message(
        request: CreateSecretMessageRequest,
        user: Annotated[User, Depends(current_active_user)],
        service: Annotated[SecretMessageService, Depends(get_service)]
):
    return await service.create_secret_message(user, request)




@router.post(path="/newest")
async def get_message(
        request: GetSecretMessageRequest,
        user: Annotated[User, Depends(current_active_user)],
        service: Annotated[SecretMessageService, Depends(get_service)]
):
    return await service.get_message(user, request)
