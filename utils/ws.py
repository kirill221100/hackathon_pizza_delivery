from typing import Dict, List
from fastapi import WebSocket, WebSocketDisconnect, status


class ConnectionManager:
    def __init__(self):
        self.__connections: Dict[int, List[WebSocket]] = {}

    async def connect(self, order_id: int, ws: WebSocket):
        if not self.__connections.get(order_id):
            self.__connections[order_id] = [ws]
        else:
            self.__connections[order_id].append(ws)
        await ws.accept()

    async def send_message(self, order_id: int, message: dict):
        [await ws.send_json(message) for ws in self.__connections[order_id]]

    async def send_text(self, order_id: int, message: str):
        [await ws.send_text(message) for ws in self.__connections[order_id]]

    async def disconnect(self, order_id: int, ws: WebSocket, close_code: int = status.WS_1000_NORMAL_CLOSURE):
        self.__connections[order_id].remove(ws)


manager = ConnectionManager()
