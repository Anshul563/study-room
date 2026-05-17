from fastapi import APIRouter, Depends

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.room_summary import (
    RoomSummary
)

router = APIRouter(
    prefix="/summaries",
    tags=["Summaries"]
)

@router.get("/{room_id}")
def get_room_summaries(
    room_id: str,
    db: Session = Depends(get_db)
):

    summaries = db.query(
        RoomSummary
    ).filter(
        RoomSummary.room_id == room_id
    ).order_by(
        RoomSummary.created_at.desc()
    ).all()

    return summaries