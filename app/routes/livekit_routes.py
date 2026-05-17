from fastapi import APIRouter, Depends

from livekit import api

from app.config import settings
from app.auth.dependencies import get_current_user
from app.models.user import User

router = APIRouter(
    prefix="/livekit",
    tags=["LiveKit"]
)

@router.get("/token/{room_name}")
def create_token(
    room_name: str,
    current_user: User = Depends(get_current_user)
):

    token = api.AccessToken(
        settings.LIVEKIT_API_KEY,
        settings.LIVEKIT_API_SECRET
    )

    token.with_identity(
        str(current_user.id)
    )

    token.with_name(
        current_user.username
    )

    token.with_grants(
        api.VideoGrants(
            room_join=True,
            room=room_name
        )
    )

    jwt_token = token.to_jwt()

    return {
        "token": jwt_token,
        "url": settings.LIVEKIT_URL
    }