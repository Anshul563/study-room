from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db

from app.models.message import Message

router = APIRouter(
    prefix="/messages",
    tags=["Messages"]
)

@router.get("/{room_id}")
def get_room_messages(
    room_id: int,
    db: Session = Depends(get_db)
):

    messages = db.query(Message).filter(
        Message.room_id == room_id
    ).order_by(
        Message.created_at.asc()
    ).all()

    return messages