import uuid
from datetime import datetime

from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from api.db.base import Base


class SecretMessageModel(Base):
    __tablename__ = "secret_messages"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4,
    )

    author_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))
    place_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True))

    content: Mapped[str]

    created_date: Mapped[datetime] = mapped_column(default=datetime.utcnow)
