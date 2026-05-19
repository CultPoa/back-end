from uuid import UUID

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.db.models.badges import BadgeModel
from api.repository.abstract_repository import AbstractRepository


class BadgeRepository(AbstractRepository[BadgeModel]):
    def __init__(self, session: AsyncSession):
        super().__init__(BadgeModel, session)

    async def find_all_by_user(
        self,
        user_id: UUID,
        limit: int = 20,
        offset: int = 0,
    ) -> list[BadgeModel]:
        result = await self._session.execute(
            select(BadgeModel)
            .where(BadgeModel.user_id == user_id)
            .offset(offset)
            .limit(limit),
        )
        return list(result.scalars().all())

    async def find_by_user_and_place(
        self,
        user_id: UUID,
        place_id: UUID,
    ) -> BadgeModel | None:
        result = await self._session.execute(
            select(BadgeModel).where(
                BadgeModel.user_id == user_id,
                BadgeModel.place_id == place_id,
            ),
        )
        return result.scalar_one_or_none()
