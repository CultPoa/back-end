from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from api.db.models.secret_messages import SecretMessageModel
from api.repository.abstract_repository import AbstractRepository


class SecretMessageRepository(AbstractRepository[SecretMessageModel]):

    def __init__(self, session: AsyncSession) -> None:
        super().__init__(model=SecretMessageModel, session=session)

    async def find_by_place_id_ordered_by_created_date(self, place_id) -> list[SecretMessageModel]:

            result = await self._session.execute(
                select(SecretMessageModel)
                .where(SecretMessageModel.place_id == place_id)
                .order_by(SecretMessageModel.created_date.desc())
                .limit(1)
            )

            return result.scalars().all()
