from uuid import UUID

from fastapi import HTTPException

from api.db.models.badges import BadgeModel
from api.db.models.places import PlaceModel
from api.db.models.users import User
from api.repository.badge_repository import BadgeRepository
from api.repository.place_repository import PlaceRepository
from api.web.api.badges.schemas import BadgeListResponse


class BadgeService:
    def __init__(
        self,
        badge_repository: BadgeRepository,
        place_repository: PlaceRepository,
    ):
        self.badge_repository = badge_repository
        self.place_repository = place_repository

    async def unlock_badge(
        self,
        user: User,
        place_id: UUID,
    ) -> BadgeModel:
        place = await self.place_repository.find_by_id(place_id)

        if place is None:
            raise HTTPException(status_code=404, detail="place not found")

        existing = await self.badge_repository.find_by_user_and_place(
            user.id,
            place_id,
        )

        if existing is not None:
            return existing

        badge = BadgeModel(
            id=None,
            user_id=user.id,
            place_id=place.id,
            place_name=place.name,
            place_type=place.type,
            lat=place.lat,
            lon=place.lon,
        )

        return await self.badge_repository.save(badge)

    async def list_user_badges(
        self,
        user: User,
        limit: int = 20,
        offset: int = 0,
    ) -> BadgeListResponse:

        badges: list[BadgeModel] = await self.badge_repository.find_all_by_user(
            user.id,
            limit,
            offset,
        )
        total: int = await self.place_repository.count_all()
        unlocked: int = len(badges)

        badges_list = [
            {
                "name": badge.place_name,
                "type": badge.place_type,
                "createdDate": badge.created_date,
            }
            for badge in badges
        ]

        return BadgeListResponse(total=total, unlocked=unlocked, badges=badges_list)
