from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.room import Room
from app.models.room_member import RoomMember
from app.schemas.room import CreateRoomSchema
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/rooms",
    tags=["Rooms"]
)

@router.post("/")
def create_room(
    room: CreateRoomSchema,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    new_room = Room(
        title=room.title,
        description=room.description,
        owner_id=current_user.id
    )

    db.add(new_room)
    db.commit()
    db.refresh(new_room)

    room_member = RoomMember(
        user_id=current_user.id,
        room_id=new_room.id
    )

    db.add(room_member)
    db.commit()

    return {
        "message": "Room created",
        "room": {
            "id": new_room.id,
            "title": new_room.title
        }
    }

@router.get("/")
def get_rooms(
    db: Session = Depends(get_db)
):

    rooms = db.query(Room).all()

    return rooms

@router.post("/{room_id}/join")
def join_room(
    room_id: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):

    room = db.query(Room).filter(
        Room.id == room_id
    ).first()

    if not room:
        raise HTTPException(
            status_code=404,
            detail="Room not found"
        )

    existing_member = db.query(RoomMember).filter(
        RoomMember.user_id == current_user.id,
        RoomMember.room_id == room_id
    ).first()

    if existing_member:
        return {
            "message": "Already joined"
        }

    member = RoomMember(
        user_id=current_user.id,
        room_id=room_id
    )

    db.add(member)
    db.commit()

    return {
        "message": "Joined room successfully"
    }