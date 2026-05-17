from fastapi import FastAPI
from app.database import Base, engine
from app.auth.auth_routes import router as auth_router
from app.routes.user_routes import router as user_router
from app.routes.room_routes import router as room_router
from app.models.room import Room
from app.models.room_member import RoomMember
from app.models.message import Message
from app.models.room_summary import RoomSummary
from app.routes.livekit_routes import router as livekit_router
from app.websocket.chat_socket import router as websocket_router
from app.routes.ai_routes import router as ai_router
from app.routes.message_routes import (
    router as message_router
)
from app.scheduler import start_scheduler
from app.routes.summary_routes import (
    router as summary_router
)
from app.models.file import File
from app.routes.file_routes import (
    router as file_router
)
from app.routes.pdf_ai_routes import (
    router as pdf_ai_router
)
from app.rag.setup_qdrant import (
    create_collection
)

Base.metadata.create_all(bind=engine)

app = FastAPI()

create_collection()

start_scheduler()

app.include_router(auth_router)
app.include_router(user_router)
app.include_router(room_router)
app.include_router(livekit_router)
app.include_router(websocket_router)
app.include_router(ai_router)
app.include_router(message_router)
app.include_router(summary_router)
app.include_router(file_router)
app.include_router(pdf_ai_router)

@app.get("/")
def root():
    return {
        "message": "AI Study Room Backend Running"
    }