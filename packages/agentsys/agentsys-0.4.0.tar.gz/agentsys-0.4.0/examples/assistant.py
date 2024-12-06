from typing import Any, Dict, List, Optional
from agentsys.core import Agent
from agentsys.core.llm import get_llm_client
from agentsys.middleware.cache import cache_response
from agentsys.middleware.retry import with_retry
from agentsys.middleware.telemetry import with_telemetry
from agentsys.protocols.messaging import MessageBus, MessageType, Message
from agentsys.plugins.router import AgentRouter, Route, Task
from agentsys.plugins.storage import FileStorage, StorageConfig
import asyncio
import json
import os
from datetime import datetime
from enum import Enum
from locksys import Locksys

class TaskType(str, Enum):
    RESEARCH = "research"
    ANALYSIS = "analysis"
    WRITING = "writing"
    CODING = "coding"

# Set OPENAI_API_KEY from env
if "OPENAI_API_KEY" not in os.environ:
    os.environ["OPENAI_API_KEY"] = Locksys().item("OPEN-AI").key("Mamba").results()

class AssistantAgent(Agent):
    """An intelligent assistant agent that can handle various tasks"""
    
    def __init__(self, name: str = "Assistant", **kwargs):
        super().__init__(
            name=name,
            description="An intelligent assistant that can handle various tasks",
            **kwargs
        )
        # Create data directory if it doesn't exist
        data_dir = os.path.join(os.getcwd(), "data", "assistant")
        os.makedirs(data_dir, exist_ok=True)
        
        self.message_bus = MessageBus()
        self.router = AgentRouter()
        self.storage = FileStorage(
            dict,
            StorageConfig(storage_path=data_dir)
        )
        self.task_history: List[Dict[str, Any]] = []
        self.llm = get_llm_client()
    
    async def initialize(self) -> None:
        """Initialize the assistant"""
        await super().initialize()
        await self.message_bus.start()
        
        # Load previous task history
        try:
            history = await self.storage.get("task_history")
            if history:
                self.task_history = history.get("tasks", [])
        except Exception as e:
            print(f"Warning: Could not load task history: {e}")
        
        # Register routes for different task types
        for task_type in TaskType:
            self.router.register_route(Route(
                pattern=f"task.{task_type.value}",
                agent_type=self.__class__,
                capabilities=[task_type.value]
            ))
        
        # Subscribe to task requests
        self.message_bus.subscribe_to_commands(
            MessageType.TASK_REQUEST,
            self._handle_task_request
        )
    
    async def _handle_task_request(self, message: Message) -> None:
        """Handle incoming task requests"""
        task = Task.parse_obj(message.content)
        route = self.router.find_route(task.type)
        if route:
            await self.execute(task.content)
    
    @with_telemetry("execute_task")
    @with_retry()
    @cache_response()
    async def execute(self, input_data: Any) -> Any:
        """Execute a task"""
        try:
            self.state = "running"
            
            # Determine task type
            task_type = (
                TaskType.CODING if isinstance(input_data, dict) and input_data.get("type") == "coding"
                else TaskType.WRITING if isinstance(input_data, str) and any(word in input_data.lower() for word in ["write", "compose", "draft"])
                else TaskType.ANALYSIS if isinstance(input_data, str) and any(word in input_data.lower() for word in ["analyze", "analyse", "study"])
                else TaskType.RESEARCH
            )
            
            # Process task
            result = await self._process_task(task_type, input_data)
            
            # Create task record
            task_record = {
                "id": str(len(self.task_history) + 1),
                "timestamp": datetime.utcnow().isoformat(),
                "type": task_type.value,
                "input": input_data,
                "result": result
            }
            
            # Add to history
            self.task_history.append(task_record)
            
            # Store in persistent storage
            await self.storage.put("task_history", {
                "tasks": self.task_history,
                "last_updated": datetime.utcnow().isoformat()
            })
            
            # For research tasks, store detailed results separately
            if task_type == TaskType.RESEARCH:
                await self.storage.put(
                    f"research_{task_record['id']}",
                    {
                        "query": input_data,
                        "result": result,
                        "timestamp": task_record["timestamp"],
                        "metadata": {
                            "source": "assistant",
                            "version": "0.3.0"
                        }
                    }
                )
            
            self.state = "completed"
            return result
        
        except Exception as e:
            self.state = "error"
            raise e
    
    async def _process_task(self, task_type: TaskType, input_data: Any) -> Any:
        """Process a specific task type"""
        if task_type == TaskType.CODING:
            return await self._handle_coding_task(input_data)
        elif task_type == TaskType.WRITING:
            return await self._handle_writing_task(input_data)
        elif task_type == TaskType.ANALYSIS:
            return await self._handle_analysis_task(input_data)
        else:  # RESEARCH
            return await self._handle_research_task(input_data)
    
    async def _handle_coding_task(self, task: Dict[str, Any]) -> str:
        """Handle a coding task"""
        messages = [
            {
                "role": "system",
                "content": """You are a Python programming expert. Your task is to write clear, efficient, and well-documented Python code.
Follow these guidelines:
1. Use type hints
2. Write clear docstrings
3. Include helpful comments
4. Add example usage
5. Follow PEP 8 style
6. Use modern Python features
7. Consider edge cases
8. Focus on readability"""
            },
            {
                "role": "user",
                "content": task["content"]
            }
        ]
        
        return await self.llm.complete(messages)
    
    async def _handle_writing_task(self, topic: str) -> str:
        """Handle a writing task"""
        messages = [
            {
                "role": "system",
                "content": """You are an expert writer. Your task is to write clear, engaging, and informative content.
Follow these guidelines:
1. Use markdown formatting
2. Create clear structure with headings
3. Include relevant examples
4. Be concise but thorough
5. Use active voice
6. Maintain professional tone
7. Add proper citations if needed
8. End with a conclusion"""
            },
            {
                "role": "user",
                "content": topic
            }
        ]
        
        return await self.llm.complete(messages)
    
    async def _handle_analysis_task(self, data: str) -> str:
        """Handle an analysis task"""
        messages = [
            {
                "role": "system",
                "content": """You are an expert analyst. Your task is to provide clear, data-driven analysis.
Follow these guidelines:
1. Use markdown formatting
2. Start with key findings
3. Include relevant data
4. Identify trends
5. Discuss challenges
6. Make recommendations
7. Consider future implications
8. Use visual descriptions when possible"""
            },
            {
                "role": "user",
                "content": data
            }
        ]
        
        return await self.llm.complete(messages)
    
    async def _handle_research_task(self, topic: str) -> str:
        """Handle a research task"""
        messages = [
            {
                "role": "system",
                "content": """You are an expert researcher. Your task is to provide comprehensive research findings.
Follow these guidelines:
1. Use markdown formatting
2. Cover historical context
3. Discuss key developments
4. Identify major contributors
5. Explain core concepts
6. Address current challenges
7. Consider future directions
8. Include timeline of events"""
            },
            {
                "role": "user",
                "content": topic
            }
        ]
        
        return await self.llm.complete(messages)
    
    async def get_task_history(self) -> List[Dict[str, Any]]:
        """Get the task execution history"""
        try:
            history = await self.storage.get("task_history")
            return history.get("tasks", [])
        except Exception as e:
            print(f"Warning: Could not load task history: {e}")
            return []
    
    async def get_research_results(self, research_id: Optional[str] = None) -> Any:
        """Get research results by ID or all research results"""
        if research_id:
            return await self.storage.get(f"research_{research_id}")
        else:
            # Get all research tasks from history
            history = await self.get_task_history()
            research_tasks = [
                task for task in history
                if task["type"] == TaskType.RESEARCH.value
            ]
            return research_tasks
    
    async def cleanup(self) -> None:
        """Cleanup resources"""
        # Save final task history
        try:
            await self.storage.put("task_history", {
                "tasks": self.task_history,
                "last_updated": datetime.utcnow().isoformat()
            })
            # Wait for storage to close properly
            await self.storage.close()
        except Exception as e:
            print(f"Warning: Could not save task history: {e}")
        
        # Close LLM client
        await self.llm.close()
        
        await self.message_bus.stop()
        await super().cleanup()


async def main():
    # Create and initialize assistant
    assistant = AssistantAgent()
    await assistant.initialize()
    
    try:
        # Example tasks
        tasks = [
            {"type": "coding", "content": "Write a Python function to calculate the circumference of Earth"}
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