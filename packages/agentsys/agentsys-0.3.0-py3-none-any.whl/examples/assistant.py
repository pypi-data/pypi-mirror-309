from typing import Any, Dict, List, Optional
from ..core.agent import TaskAgent
from ..middleware.cache import cache_response
from ..middleware.retry import with_retry
from ..middleware.telemetry import with_telemetry
from ..protocols.messaging import MessageBus, MessageType, Message
from ..plugins.router import AgentRouter, Route, Task
from ..plugins.storage import FileStorage, StorageConfig
import asyncio
import json
from datetime import datetime
from enum import Enum

class TaskType(str, Enum):
    RESEARCH = "research"
    ANALYSIS = "analysis"
    WRITING = "writing"
    CODING = "coding"

class AssistantAgent(TaskAgent):
    """An intelligent assistant agent that can handle various tasks"""
    
    def __init__(self, name: str = "Assistant", **kwargs):
        super().__init__(
            name=name,
            description="An intelligent assistant that can handle various tasks",
            **kwargs
        )
        self.message_bus = MessageBus()
        self.router = AgentRouter()
        self.storage = FileStorage(
            dict,
            StorageConfig(storage_path="./data/assistant")
        )
        self.task_history: List[Dict[str, Any]] = []
    
    async def initialize(self) -> None:
        """Initialize the assistant"""
        await super().initialize()
        await self.message_bus.start()
        
        # Register routes for different task types
        for task_type in TaskType:
            self.router.register_route(Route(
                pattern=f"task.{task_type.value}",
                agent_type=self.__class__,
                capabilities=[task_type.value]
            ))
        
        # Subscribe to task requests
        self.message_bus.subscribe_to_commands(
            self.id,
            "task.*",
            self._handle_task_request
        )
    
    @cache_response(ttl=3600)
    @with_retry(max_attempts=3)
    @with_telemetry("process_task")
    async def execute(self, input_data: Any) -> Any:
        """Process a task"""
        task_type = self._determine_task_type(input_data)
        
        # Store task in history
        task_record = {
            "timestamp": datetime.utcnow(),
            "type": task_type,
            "input": input_data
        }
        self.task_history.append(task_record)
        
        # Process task based on type
        result = await self._process_task(task_type, input_data)
        
        # Update task record
        task_record["result"] = result
        task_record["completed_at"] = datetime.utcnow()
        
        # Store in persistent storage
        await self.storage.put(
            f"task_{task_record['timestamp'].isoformat()}",
            task_record
        )
        
        return result
    
    def _determine_task_type(self, input_data: Any) -> TaskType:
        """Determine the type of task from input"""
        if isinstance(input_data, dict):
            return TaskType(input_data.get("type", TaskType.RESEARCH))
        
        # Analyze input text to determine task type
        text = str(input_data).lower()
        
        if any(word in text for word in ["code", "program", "implement", "debug"]):
            return TaskType.CODING
        elif any(word in text for word in ["analyze", "evaluate", "assess"]):
            return TaskType.ANALYSIS
        elif any(word in text for word in ["write", "compose", "draft"]):
            return TaskType.WRITING
        else:
            return TaskType.RESEARCH
    
    async def _process_task(self, task_type: TaskType, input_data: Any) -> Any:
        """Process a task based on its type"""
        # Prepare system message based on task type
        system_messages = {
            TaskType.RESEARCH: "You are a research assistant helping to gather and synthesize information.",
            TaskType.ANALYSIS: "You are an analytical assistant helping to evaluate and interpret data.",
            TaskType.WRITING: "You are a writing assistant helping to create and edit content.",
            TaskType.CODING: "You are a coding assistant helping to write and debug code."
        }
        
        messages = [
            {"role": "system", "content": system_messages[task_type]},
            {"role": "user", "content": str(input_data)}
        ]
        
        # Generate response
        response = await self.client.chat.completions.create(
            model=self.config.model,
            messages=messages,
            temperature=self.config.temperature,
            max_tokens=self.config.max_tokens
        )
        
        return response.choices[0].message.content
    
    async def _handle_task_request(self, message: Message) -> None:
        """Handle incoming task requests"""
        if message.type == MessageType.COMMAND:
            task = Task(
                input_data=message.content,
                pattern=f"task.{self._determine_task_type(message.content).value}"
            )
            
            # Submit task to router
            task_id = await self.router.submit_task(task)
            
            # Wait for result
            result = await self.router.get_task_result(task_id)
            
            # Send response
            await self.message_bus.send_command(
                sender=self.id,
                recipients=[message.sender],
                command="task.completed",
                payload=result
            )
    
    async def get_task_history(
        self,
        task_type: Optional[TaskType] = None,
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """Get recent task history"""
        history = self.task_history
        if task_type:
            history = [task for task in history if task["type"] == task_type]
        return history[-limit:]
    
    async def cleanup(self) -> None:
        """Cleanup resources"""
        await self.message_bus.stop()
        await self.router.stop()
        await super().cleanup()

# Example usage
async def main():
    # Create and initialize assistant
    assistant = AssistantAgent()
    await assistant.initialize()
    
    try:
        # Example tasks
        tasks = [
            "Write a short blog post about AI",
            {"type": "coding", "content": "Write a Python function to sort a list"},
            "Analyze the trends in renewable energy",
            "Research the history of quantum computing"
        ]
        
        for task in tasks:
            print(f"\nProcessing task: {task}")
            result = await assistant.execute(task)
            print(f"Result: {result}\n")
        
        # Get task history
        history = await assistant.get_task_history()
        print("\nTask History:")
        print(json.dumps(history, default=str, indent=2))
    
    finally:
        await assistant.cleanup()

if __name__ == "__main__":
    asyncio.run(main())