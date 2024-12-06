"""Tests for the agents module."""

import pytest
from agentsys.agents import Agent
from agentsys.types import Agent

class TestBaseAgent:
    """Tests for the BaseAgent class."""

    def test_initialization_with_config(self):
        """Test agent initialization with config."""
        config = {"model": "gpt-4", "temperature": 0.7}
        agent = Agent(config=config)
        assert agent.config == config

    def test_initialization_without_config(self):
        """Test agent initialization without config."""
        agent = Agent()
        assert agent.config == {}

    def test_initialization_with_none_config(self):
        """Test agent initialization with None config."""
        agent = Agent(config=None)
        assert agent.config == {}
