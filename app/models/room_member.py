from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from nanoid import generate
from app.database import Base

class RoomMember(Base):
    __tablename__ = "room_members"

    id = Column(String, primary_key=True, default=generate)

    user_id = Column(
        String,
        ForeignKey("users.id")
    )

    room_id = Column(
        String,
        ForeignKey("rooms.id")
    )

    joined_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )