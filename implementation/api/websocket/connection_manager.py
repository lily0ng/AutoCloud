"""
WebSocket connection manager for real-time communication
"""
from typing import Dict, Set
import asyncio
import json
import logging
from datetime import datetime

logger = logging.getLogger(__name__)


class ConnectionManager:
    """Manage WebSocket connections"""
    
    def __init__(self):
        self.active_connections: Dict[str, Set] = {}
        self.user_connections: Dict[str, str] = {}
    
    async def connect(self, websocket, client_id: str, room: str = "default"):
        """Accept new WebSocket connection"""
        await websocket.accept()
        
        if room not in self.active_connections:
            self.active_connections[room] = set()
        
        self.active_connections[room].add(websocket)
        self.user_connections[client_id] = room
        
        logger.info(f"Client {client_id} connected to room {room}")
        
        # Send welcome message
        await self.send_personal_message({
            'type': 'connection',
            'message': 'Connected successfully',
            'client_id': client_id,
            'room': room,
            'timestamp': datetime.utcnow().isoformat()
        }, websocket)
    
    def disconnect(self, websocket, client_id: str):
        """Remove WebSocket connection"""
        room = self.user_connections.get(client_id)
        if room and room in self.active_connections:
            self.active_connections[room].discard(websocket)
            if not self.active_connections[room]:
                del self.active_connections[room]
        
        if client_id in self.user_connections:
            del self.user_connections[client_id]
        
        logger.info(f"Client {client_id} disconnected from room {room}")
    
    async def send_personal_message(self, message: dict, websocket):
        """Send message to specific client"""
        try:
            await websocket.send_text(json.dumps(message))
        except Exception as e:
            logger.error(f"Error sending personal message: {str(e)}")
    
    async def broadcast(self, message: dict, room: str = "default"):
        """Broadcast message to all clients in room"""
        if room not in self.active_connections:
            return
        
        message['timestamp'] = datetime.utcnow().isoformat()
        disconnected = set()
        
        for connection in self.active_connections[room]:
            try:
                await connection.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Error broadcasting message: {str(e)}")
                disconnected.add(connection)
        
        # Remove disconnected clients
        for connection in disconnected:
            self.active_connections[room].discard(connection)
    
    async def send_to_user(self, client_id: str, message: dict):
        """Send message to specific user"""
        room = self.user_connections.get(client_id)
        if not room or room not in self.active_connections:
            logger.warning(f"Client {client_id} not found")
            return
        
        for connection in self.active_connections[room]:
            try:
                await connection.send_text(json.dumps(message))
            except Exception as e:
                logger.error(f"Error sending message to user: {str(e)}")
    
    def get_room_count(self, room: str = "default") -> int:
        """Get number of connections in room"""
        return len(self.active_connections.get(room, set()))
    
    def get_total_connections(self) -> int:
        """Get total number of active connections"""
        return sum(len(conns) for conns in self.active_connections.values())


# Global connection manager instance
manager = ConnectionManager()
