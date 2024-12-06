from typing import Dict, Any, Optional, List, Callable, Union
from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from enum import Enum
import asyncio
import logging
import uuid

logger = logging.getLogger(__name__)

class MessageType(str, Enum):
    """Types of messages that can be sent"""
    COMMAND = "command"
    EVENT = "event"
    TASK_REQUEST = "task_request"
    TASK_RESPONSE = "task_response"
    ERROR = "error"

class Message(BaseModel):
    """A message that can be sent between agents"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: MessageType
    sender: str
    recipients: List[str] = Field(default_factory=list)
    content: Any
    metadata: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    
    model_config = ConfigDict(arbitrary_types_allowed=True)

class MessageBus:
    """Simple message bus for agent communication"""
    
    def __init__(self):
        self._subscribers: Dict[MessageType, List[Callable]] = {
            message_type: [] for message_type in MessageType
        }
        self._running = False
        self._message_queue: asyncio.Queue = asyncio.Queue()
        self._processing_task: Optional[asyncio.Task] = None
    
    def subscribe_to_commands(self, message_type: MessageType, handler: Callable) -> None:
        """Subscribe to messages of a specific type"""
        self._subscribers[message_type].append(handler)
        logger.info(f"Subscribed handler to {message_type}")
    
    async def send_message(self, message: Message) -> None:
        """Send a message to all subscribers"""
        await self._message_queue.put(message)
        logger.debug(f"Queued message {message.id} of type {message.type}")
    
    async def _process_messages(self) -> None:
        """Process messages from the queue"""
        while self._running:
            try:
                message = await self._message_queue.get()
                
                # Call all handlers for this message type
                handlers = self._subscribers.get(message.type, [])
                for handler in handlers:
                    try:
                        await handler(message)
                    except Exception as e:
                        logger.error(f"Error in message handler: {str(e)}")
                
                self._message_queue.task_done()
            
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")
    
    async def start(self) -> None:
        """Start the message bus"""
        if self._running:
            return
        
        self._running = True
        self._processing_task = asyncio.create_task(self._process_messages())
        logger.info("Message bus started")
    
    async def stop(self) -> None:
        """Stop the message bus"""
        if not self._running:
            return
        
        self._running = False
        if self._processing_task:
            self._processing_task.cancel()
            try:
                await self._processing_task
            except asyncio.CancelledError:
                pass
        
        logger.info("Message bus stopped")