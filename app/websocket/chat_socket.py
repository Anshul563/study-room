from fastapi import (
    APIRouter,
    WebSocket,
    WebSocketDisconnect
)

from sqlalchemy.orm import Session

from app.websocket.manager import manager

from app.database import SessionLocal

from app.models.message import Message

router = APIRouter()

@router.websocket("/ws/chat/{room_id}/{username}")
async def websocket_chat(
    websocket: WebSocket,
    room_id: str,
    username: str
):

    await manager.connect(
        room_id,
        websocket,
        username
    )

    await manager.send_online_users(
        room_id
    )

    db: Session = SessionLocal()

    try:

        while True:

            data = await websocket.receive_json()

            message_type = data.get("type")

            # Typing Indicator
            if message_type == "typing":

                await manager.broadcast(
                    room_id,
                    {
                        "type": "typing",
                        "username": username
                    }
                )

                continue

            # Chat Message
            new_message = Message(
                room_id=room_id,
                user_id=data["user_id"],
                username=username,
                content=data["message"]
            )

            db.add(new_message)

            db.commit()

            db.refresh(new_message)

            await manager.broadcast(
                room_id,
                {
                    "type": "message",
                    "id": new_message.id,
                    "username": username,
                    "message": new_message.content,
                    "created_at": str(
                        new_message.created_at
                    )
                }
            )

    except WebSocketDisconnect:
        pass
    except Exception as e:
        print(f"WebSocket error in room {room_id}: {e}")
    finally:
        manager.disconnect(
            room_id,
            websocket,
            username
        )

        try:
            await manager.send_online_users(
                room_id
            )
        except Exception:
            pass

        db.close()