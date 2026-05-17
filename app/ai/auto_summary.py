from sqlalchemy.orm import Session

from app.database import SessionLocal

from app.models.room import Room

from app.models.message import Message

from app.models.room_summary import (
    RoomSummary
)

from app.ai.summary_service import (
    generate_room_summary
)

def generate_auto_summaries():

    db: Session = SessionLocal()

    try:

        rooms = db.query(Room).all()

        for room in rooms:

            messages = db.query(Message).filter(
                Message.room_id == room.id
            ).order_by(
                Message.created_at.desc()
            ).limit(50).all()

            if not messages:
                continue

            message_texts = [
                f"{msg.username}: {msg.content}"
                for msg in messages
            ]

            summary = generate_room_summary(
                message_texts
            )

            new_summary = RoomSummary(
                room_id=room.id,
                summary=summary
            )

            db.add(new_summary)

        db.commit()

        print("AI summaries generated")

    finally:

        db.close()