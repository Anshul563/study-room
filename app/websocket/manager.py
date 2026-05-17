from fastapi import WebSocket

class ConnectionManager:

    def __init__(self):

        self.active_connections = {}

        self.online_users = {}

    async def connect(
        self,
        room_id: str,
        websocket: WebSocket,
        username: str
    ):

        await websocket.accept()

        if room_id not in self.active_connections:
            self.active_connections[room_id] = []

        if room_id not in self.online_users:
            self.online_users[room_id] = []

        self.active_connections[room_id].append(
            websocket
        )

        self.online_users[room_id].append(
            username
        )

    def disconnect(
        self,
        room_id: str,
        websocket: WebSocket,
        username: str
    ):

        self.active_connections[room_id].remove(
            websocket
        )

        if username in self.online_users[room_id]:

            self.online_users[room_id].remove(
                username
            )

    async def broadcast(
        self,
        room_id: str,
        message: dict
    ):

        for connection in self.active_connections.get(
            room_id,
            []
        ):

            await connection.send_json(message)

    async def send_online_users(
        self,
        room_id: str
    ):

        await self.broadcast(
            room_id,
            {
                "type": "online_users",
                "users": self.online_users.get(
                    room_id,
                    []
                )
            }
        )

manager = ConnectionManager()