"""AgentSys core system implementation"""

from typing import List, Dict, Any
from .agent import Agent

class AgentSys:
    """Simple wrapper for running agent conversations."""
    def run(self, agent: Agent, messages: List[Dict[str, str]]) -> Dict[str, Any]:
        """Run a conversation with an agent."""
        return agent.run(messages)

def run(agent: Agent, messages: List[Dict[str, str]]) -> Dict[str, Any]:
    """Convenience function to run an agent conversation."""
    return AgentSys().run(agent=agent, messages=messages)
