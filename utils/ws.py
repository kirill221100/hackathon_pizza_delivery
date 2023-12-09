from typing import Dict, List
from fastapi import WebSocket, WebSocketDisconnect, status


class UsersOrdersManager:
    def __init__(self):
        self.__connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, user_id: int, ws: WebSocket):
        if not self.__connections.get(user_id):
            self.__connections[user_id] = [ws]
        else:
            self.__connections[user_id].append(ws)
        await ws.accept()

    async def send_data(self, user_id: int, data: dict):
        [await ws.send_json(data) for ws in self.__connections[user_id]]

    async def disconnect(self, user_id: int, ws: WebSocket):
        self.__connections[user_id].remove(ws)


users_orders_manager = UsersOrdersManager()