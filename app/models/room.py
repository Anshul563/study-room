from sqlalchemy import Column, String, ForeignKey, DateTime
from sqlalchemy.sql import func
from nanoid import generate
from app.database import Base

class Room(Base):
    __tablename__ = "rooms"

    id = Column(String, primary_key=True, index=True, default=generate)

    title = Column(String, nullable=False)

    description = Column(String, nullable=True)

    owner_id = Column(
        String,
        ForeignKey("users.id")
    )

    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )