from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)

from sqlalchemy.sql import func

from app.database import Base

class RoomSummary(Base):

    __tablename__ = "room_summaries"

    id = Column(
        Integer,
        primary_key=True
    )

    room_id = Column(
        Integer,
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