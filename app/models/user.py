from sqlalchemy import Column, String
from nanoid import generate
from app.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(String, primary_key=True, index=True, default=generate)
    username = Column(String, nullable=False)
    email = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    google_id = Column(String, nullable=True)
    avatar = Column(String, nullable=True)