from typing import Dict, List
from fastapi import WebSocket, WebSocketDisconnect, status


class ConnectionManager:
    def __init__(self):
        self.__connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, user_id: int, ws: WebSocket):
        if not self.__connections.get(user_id):
            self.__connections[user_id] = [ws]
        self.__connections[user_id].append(ws)
        await ws.accept()

    async def send_message(self, user_id: int, message: dict):
        [await ws.send_json(message) for ws in self.__connections[user_id]]

    async def send_text(self, user_id: int, message: str):
        [await ws.send_text(message) for ws in self.__connections[user_id]]

    async def disconnect(self, user_id: int, ws: WebSocket, close_code: int = status.WS_1000_NORMAL_CLOSURE):
        self.__connections[user_id].remove(ws)
        await ws.close(code=close_code)


manager = ConnectionManager()
