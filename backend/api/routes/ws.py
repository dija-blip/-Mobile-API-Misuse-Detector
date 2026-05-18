from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from backend.core.websocket import manager

router = APIRouter(tags=["websocket"])


@router.websocket("/ws/live")
async def live_feed(ws: WebSocket):
    await manager.connect(ws)
    try:
        while True:
            await ws.receive_text()  # keep connection alive
    except WebSocketDisconnect:
        manager.disconnect(ws)
