from pydantic import BaseModel

class CreateRoomSchema(BaseModel):
    title: str
    description: str | None = None