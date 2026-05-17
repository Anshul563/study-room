from sqlalchemy import (
    Column,
    Integer,
    String,
    ForeignKey,
    DateTime
)

from sqlalchemy.sql import func

from app.database import Base

class File(Base):

    __tablename__ = "files"

    id = Column(
        Integer,
        primary_key=True
    )

    room_id = Column(
        Integer,
        ForeignKey("rooms.id")
    )

    user_id = Column(
        Integer,
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