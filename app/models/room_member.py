from sqlalchemy import Column, Integer, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.database import Base

class RoomMember(Base):
    __tablename__ = "room_members"

    id = Column(Integer, primary_key=True)

    user_id = Column(
        Integer,
        ForeignKey("users.id")
    )

    room_id = Column(
        Integer,
        ForeignKey("rooms.id")
    )

    joined_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )