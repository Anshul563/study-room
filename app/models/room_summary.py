from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    DateTime
)

from sqlalchemy.sql import func
from nanoid import generate

from app.database import Base

class RoomSummary(Base):

    __tablename__ = "room_summaries"

    id = Column(
        String,
        primary_key=True,
        default=generate
    )

    room_id = Column(
        String,
        ForeignKey("rooms.id")
    )

    summary = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )