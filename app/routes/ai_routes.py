from fastapi import APIRouter, Depends

from app.ai.summary_service import (
    generate_room_summary
)

from app.auth.dependencies import (
    get_current_user
)

from app.models.user import User

router = APIRouter(
    prefix="/ai",
    tags=["AI"]
)

@router.post("/summary")
def create_summary(
    payload: dict,
    current_user: User = Depends(get_current_user)
):

    messages = payload.get("messages", [])

    summary = generate_room_summary(
        messages
    )

    return {
        "summary": summary
    }