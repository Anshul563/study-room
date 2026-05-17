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
    room_id: int,

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
    room_id: int,
    db: Session = Depends(get_db)
):

    files = db.query(FileModel).filter(
        FileModel.room_id == room_id
    ).all()

    return files