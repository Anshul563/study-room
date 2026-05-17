from sqlalchemy import (
    Column,
    String,
    ForeignKey,
    DateTime
)

from sqlalchemy.sql import func
from nanoid import generate

from app.database import Base

class File(Base):

    __tablename__ = "files"

    id = Column(
        String,
        primary_key=True,
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

    filename = Column(
        String,
        nullable=False
    )

    file_url = Column(
        String,
        nullable=False
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )