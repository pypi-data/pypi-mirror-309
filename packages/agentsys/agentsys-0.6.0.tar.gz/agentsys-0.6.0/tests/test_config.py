"""Tests for the config module."""

import pytest
from agentsys.config import Settings

class TestSettings:
    """Tests for the Settings class."""

    def test_initialization_with_config(self):
        """Test settings initialization with config."""
        config = {"api_key": "test_key", "model": "gpt-4"}
        settings = Settings(config=config)
        assert settings.config == config

    def test_initialization_without_config(self):
        """Test settings initialization without config."""
        settings = Settings()
        assert settings.config == {}

    def test_config_property(self):
        """Test that config property returns a copy."""
        config = {"api_key": "test_key"}
        settings = Settings(config=config)
        
        # Get config and modify it
        config_copy = settings.config
        config_copy["new_key"] = "new_value"
        
        # Original config should be unchanged
        assert "new_key" not in settings.config
