from typing import Annotated, List

from fastapi import APIRouter, Depends, Response, status
from sqlalchemy.ext.asyncio import AsyncSession

from api.db.dependencies import get_db_session
from api.db.models.badges import BadgeModel
from api.db.models.users import User, current_active_user
from api.repository.badge_repository import BadgeRepository
from api.repository.place_repository import PlaceRepository
from api.services.badge_service import BadgeService
from api.web.api.badges.schemas import BadgeUnlockRequest, BadgeListResponse

router = APIRouter()


def get_service(
    session: Annotated[AsyncSession, Depends(get_db_session)],
) -> BadgeService:
    return BadgeService(
        BadgeRepository(session),
        PlaceRepository(session),
    )


@router.post("/badge", status_code=status.HTTP_204_NO_CONTENT)
async def unlock_badge(
    payload: BadgeUnlockRequest,
    user: Annotated[User, Depends(current_active_user)],
    service: Annotated[BadgeService, Depends(get_service)],
):
    await service.unlock_badge(user, payload.placeId)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.get("/badge", response_model=BadgeListResponse)  # Added response_model
async def list_badges(
    user: Annotated[User, Depends(current_active_user)],
    service: Annotated[BadgeService, Depends(get_service)],
):
    return await service.list_user_badges(user)
