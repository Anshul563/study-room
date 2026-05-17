from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    DateTime
)

from sqlalchemy.sql import func
from nanoid import generate

from app.database import Base

class Message(Base):

    __tablename__ = "messages"

    id = Column(
        String,
        primary_key=True,
        index=True,
        default=generate
    )

    room_id = Column(
        String,
        ForeignKey("rooms.id")
    )

    user_id = Column(
        String,
        ForeignKey("users.id")
    )

    username = Column(
        String,
        nullable=False
    )

    content = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )