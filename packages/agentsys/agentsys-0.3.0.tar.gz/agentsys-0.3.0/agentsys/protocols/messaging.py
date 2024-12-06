from typing import Dict, Any, Optional, List, Callable, Union
from pydantic import BaseModel, Field
import asyncio
import logging
from datetime import datetime
import uuid
from enum import Enum

logger = logging.getLogger(__name__)

class MessageType(str, Enum):
    COMMAND = "command"
    EVENT = "event"
    QUERY = "query"
    RESPONSE = "response"
    ERROR = "error"

class MessagePriority(int, Enum):
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3

class Message(BaseModel):
    """Represents a message in the system"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    type: MessageType
    sender: str
    recipients: List[str]
    subject: str
    content: Any
    priority: MessagePriority = MessagePriority.NORMAL
    correlation_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)
    metadata: Dict[str, Any] = {}

class Subscription(BaseModel):
    """Represents a message subscription"""
    pattern: str
    callback: Callable[[Message], None]
    filters: Dict[str, Any] = {}

class MessageBroker:
    """Handles message routing and delivery"""
    
    def __init__(self):
        self._subscriptions: Dict[str, List[Subscription]] = {}
        self._message_queue: asyncio.Queue[Message] = asyncio.Queue()
        self._processing_task: Optional[asyncio.Task] = None
        self._active = False
    
    def subscribe(self, subscriber_id: str, subscription: Subscription) -> None:
        """Subscribe to messages"""
        if subscriber_id not in self._subscriptions:
            self._subscriptions[subscriber_id] = []
        self._subscriptions[subscriber_id].append(subscription)
    
    def unsubscribe(self, subscriber_id: str, pattern: Optional[str] = None) -> None:
        """Unsubscribe from messages"""
        if pattern:
            self._subscriptions[subscriber_id] = [
                sub for sub in self._subscriptions.get(subscriber_id, [])
                if sub.pattern != pattern
            ]
        else:
            self._subscriptions.pop(subscriber_id, None)
    
    async def publish(self, message: Message) -> None:
        """Publish a message"""
        await self._message_queue.put(message)
    
    def _matches_pattern(self, subject: str, pattern: str) -> bool:
        """Check if subject matches subscription pattern"""
        if pattern == "*":
            return True
        return subject == pattern or (
            pattern.endswith("*") and
            subject.startswith(pattern[:-1])
        )
    
    def _matches_filters(self, message: Message, filters: Dict[str, Any]) -> bool:
        """Check if message matches subscription filters"""
        for key, value in filters.items():
            if key == "type" and message.type != value:
                return False
            if key == "priority" and message.priority < value:
                return False
            if key == "sender" and message.sender != value:
                return False
        return True
    
    async def _process_message(self, message: Message) -> None:
        """Process and deliver a message to subscribers"""
        delivered = False
        
        for subscriber_id, subscriptions in self._subscriptions.items():
            if subscriber_id in message.recipients or not message.recipients:
                for subscription in subscriptions:
                    if (self._matches_pattern(message.subject, subscription.pattern) and
                        self._matches_filters(message, subscription.filters)):
                        try:
                            await asyncio.to_thread(subscription.callback, message)
                            delivered = True
                        except Exception as e:
                            logger.error(
                                f"Error delivering message {message.id} to subscriber {subscriber_id}: {str(e)}"
                            )
        
        if not delivered:
            logger.warning(f"No subscribers found for message {message.id}")
    
    async def start(self) -> None:
        """Start the message broker"""
        self._active = True
        self._processing_task = asyncio.create_task(self._process_queue())
    
    async def stop(self) -> None:
        """Stop the message broker"""
        self._active = False
        if self._processing_task:
            self._processing_task.cancel()
            try:
                await self._processing_task
            except asyncio.CancelledError:
                pass
    
    async def _process_queue(self) -> None:
        """Process messages from the queue"""
        while self._active:
            try:
                message = await self._message_queue.get()
                await self._process_message(message)
                self._message_queue.task_done()
            except asyncio.CancelledError:
                break
            except Exception as e:
                logger.error(f"Error processing message queue: {str(e)}")

class MessageBus:
    """High-level message bus for agent communication"""
    
    def __init__(self):
        self._broker = MessageBroker()
        self._response_futures: Dict[str, asyncio.Future] = {}
    
    async def start(self) -> None:
        """Start the message bus"""
        await self._broker.start()
    
    async def stop(self) -> None:
        """Stop the message bus"""
        await self._broker.stop()
    
    async def send_command(
        self,
        sender: str,
        recipients: List[str],
        command: str,
        payload: Any,
        priority: MessagePriority = MessagePriority.NORMAL
    ) -> None:
        """Send a command message"""
        message = Message(
            type=MessageType.COMMAND,
            sender=sender,
            recipients=recipients,
            subject=f"command.{command}",
            content=payload,
            priority=priority
        )
        await self._broker.publish(message)
    
    async def query(
        self,
        sender: str,
        recipients: List[str],
        query: str,
        payload: Any,
        timeout: float = 30.0
    ) -> Any:
        """Send a query and wait for response"""
        message = Message(
            type=MessageType.QUERY,
            sender=sender,
            recipients=recipients,
            subject=f"query.{query}",
            content=payload,
            correlation_id=str(uuid.uuid4())
        )
        
        future = asyncio.Future()
        self._response_futures[message.correlation_id] = future
        
        try:
            await self._broker.publish(message)
            return await asyncio.wait_for(future, timeout)
        finally:
            self._response_futures.pop(message.correlation_id, None)
    
    def subscribe_to_commands(
        self,
        subscriber_id: str,
        command_pattern: str,
        callback: Callable[[Message], None],
        priority_threshold: MessagePriority = MessagePriority.LOW
    ) -> None:
        """Subscribe to command messages"""
        self._broker.subscribe(
            subscriber_id,
            Subscription(
                pattern=f"command.{command_pattern}",
                callback=callback,
                filters={"type": MessageType.COMMAND, "priority": priority_threshold}
            )
        )
    
    def subscribe_to_queries(
        self,
        subscriber_id: str,
        query_pattern: str,
        callback: Callable[[Message], None]
    ) -> None:
        """Subscribe to query messages"""
        self._broker.subscribe(
            subscriber_id,
            Subscription(
                pattern=f"query.{query_pattern}",
                callback=callback,
                filters={"type": MessageType.QUERY}
            )
        )