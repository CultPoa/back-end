import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from api.db.base import Base


class BadgeModel(Base):
    __tablename__ = "badges"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    user_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    place_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))

    place_name: Mapped[str]
    place_type: Mapped[str]

    lat: Mapped[float]
    lon: Mapped[float]

    created_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
