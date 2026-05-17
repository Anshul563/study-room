import uuid

from fastapi import (
    APIRouter,
    UploadFile,
    File,
    Depends
)

from sqlalchemy.orm import Session

from app.database import get_db

from app.models.file import File as FileModel

from app.models.user import User

from app.auth.dependencies import (
    get_current_user
)

from app.services.r2_service import (
    upload_file_to_r2
)

router = APIRouter(
    prefix="/files",
    tags=["Files"]
)

@router.post("/upload/{room_id}")
async def upload_file(
    room_id: str,

    file: UploadFile = File(...),

    db: Session = Depends(get_db),

    current_user: User = Depends(
        get_current_user
    )
):

    unique_filename = (
        f"{uuid.uuid4()}-{file.filename}"
    )

    file_url = upload_file_to_r2(
        file.file,
        unique_filename
    )

    new_file = FileModel(
        room_id=room_id,
        user_id=current_user.id,
        filename=file.filename,
        file_url=file_url
    )

    db.add(new_file)

    db.commit()

    db.refresh(new_file)

    return {
        "message": "File uploaded",
        "file": {
            "id": new_file.id,
            "filename": new_file.filename,
            "url": new_file.file_url
        }
    }

@router.get("/{room_id}")
def get_room_files(
    room_id: str,
    db: Session = Depends(get_db)
):

    files = db.query(FileModel).filter(
        FileModel.room_id == room_id
    ).all()

    return files

from fastapi import Form
from typing import Optional
from app.models.message import Message
from app.websocket.manager import manager

@router.post("/chat-upload/{room_id}")
async def chat_upload_file(
    room_id: str,
    file: UploadFile = File(...),
    user_id: str = Form(...),
    username: str = Form(...),
    upload_token: Optional[str] = Form(None),
    db: Session = Depends(get_db)
):
    unique_filename = f"{uuid.uuid4()}-{file.filename}"
    file_url = upload_file_to_r2(file.file, unique_filename)

    # Determine file type
    content_type = file.content_type
    if content_type and content_type.startswith("image/"):
        file_type = "image"
    elif content_type == "application/pdf":
        file_type = "pdf"
    else:
        file_type = "other"

    new_message = Message(
        room_id=room_id,
        user_id=user_id,
        username=username,
        content="",
        file_url=file_url,
        file_name=file.filename,
        file_type=file_type
    )

    db.add(new_message)
    db.commit()
    db.refresh(new_message)

    # Broadcast message to room
    await manager.broadcast(
        room_id,
        {
            "type": "message",
            "id": new_message.id,
            "username": username,
            "message": new_message.content,
            "file_url": new_message.file_url,
            "file_name": new_message.file_name,
            "file_type": new_message.file_type,
            "created_at": str(new_message.created_at)
        }
    )

    if upload_token:
        # Broadcast success event to dismiss modal
        await manager.broadcast(
            room_id,
            {
                "type": "mobile_upload_success",
                "token": upload_token
            }
        )

    return {"message": "File sent in chat", "file_url": file_url}