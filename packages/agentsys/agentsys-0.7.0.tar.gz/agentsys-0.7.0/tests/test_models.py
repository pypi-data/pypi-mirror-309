"""Tests for the models module."""

import pytest
from typing import AsyncGenerator, Dict, List, Optional, Union
from openai.types.chat import ChatCompletion, ChatCompletionMessage
from openai.types.chat.chat_completion import Choice

from agentsys.models import BaseModel, OpenAIModel
from agentsys.types import Message
from unittest.mock import Mock, patch
from openai import OpenAI
from locksys import Locksys

from tests.mock_client import create_mock_response


class ConcreteModel(BaseModel):
    """Concrete implementation of BaseModel for testing."""
    def generate(self, messages, **kwargs):
        return {"role": "assistant", "content": "test"}

    def stream(self, messages, **kwargs):
        yield {"role": "assistant", "content": "test"}


class TestBaseModel:
    """Tests for the BaseModel class."""

    def test_abstract_methods(self):
        """Test that BaseModel cannot be instantiated without implementing abstract methods."""
        with pytest.raises(TypeError):
            BaseModel()

    def test_concrete_implementation(self):
        """Test that concrete implementation can be instantiated."""
        model = ConcreteModel()
        assert isinstance(model, BaseModel)
        
        # Test generate method
        response = model.generate([{"role": "user", "content": "test"}])
        assert response["content"] == "test"
        
        # Test stream method
        stream = model.stream([{"role": "user", "content": "test"}])
        first_chunk = next(stream)
        assert first_chunk["content"] == "test"

    def test_base_model_abstract_methods_direct(self):
        """Test direct calls to BaseModel abstract methods."""
        class TestModel(BaseModel):
            def generate(self, messages, **kwargs):
                return super().generate(messages, **kwargs)
        
            def stream(self, messages, **kwargs):
                return super().stream(messages, **kwargs)

        model = TestModel()
        
        with pytest.raises(NotImplementedError):
            model.generate([{"role": "user", "content": "test"}])
        
        with pytest.raises(NotImplementedError):
            model.stream([{"role": "user", "content": "test"}])

    def test_base_model_inheritance_without_implementation(self):
        """Test inheriting from BaseModel without implementing abstract methods."""
        class IncompleteModel(BaseModel):
            pass

        with pytest.raises(TypeError) as exc_info:
            IncompleteModel()
        assert "Can't instantiate abstract class" in str(exc_info.value)

    def test_base_model_partial_implementation(self):
        """Test inheriting from BaseModel with only partial implementation."""
        class PartialModel(BaseModel):
            def generate(self, messages, **kwargs):
                return {"role": "assistant", "content": "test"}

        with pytest.raises(TypeError) as exc_info:
            PartialModel()
        assert "Can't instantiate abstract class" in str(exc_info.value)


class TestOpenAIModel:
    """Tests for the OpenAIModel implementation."""

    @pytest.fixture
    def api_key(self):
        """Get API key from Locksys."""
        return Locksys().item('OPEN-AI').key('Mamba').results()

    @pytest.fixture
    def mock_openai(self, api_key):
        with patch('openai.OpenAI') as mock:
            mock_client = Mock()
            mock.return_value = mock_client
            yield mock_client

    def test_initialization_with_client(self, api_key):
        """Test model initialization with provided client."""
        client = OpenAI(api_key=api_key)
        model = OpenAIModel(client=client)
        assert model.client == client

    def test_initialization_without_client(self, api_key):
        """Test model initialization without client."""
        with patch.dict('os.environ', {'OPENAI_API_KEY': api_key}):
            model = OpenAIModel()
            assert model.client is not None

    def test_generate(self, mock_openai):
        """Test generate method."""
        messages = [{"role": "user", "content": "Hello"}]
        expected_response = create_mock_response({"role": "assistant", "content": "Hi"})
        
        mock_openai.chat.completions.create.return_value = expected_response
        model = OpenAIModel(client=mock_openai)
        
        response = model.generate(messages, model="gpt-4")
        
        mock_openai.chat.completions.create.assert_called_once_with(
            messages=messages,
            model="gpt-4",
            stream=False
        )
        assert response == expected_response

    def test_stream(self, mock_openai):
        """Test stream method."""
        messages = [{"role": "user", "content": "Hello"}]
        expected_response = create_mock_response({"role": "assistant", "content": "Hi"})
        
        mock_openai.chat.completions.create.return_value = [expected_response]
        model = OpenAIModel(client=mock_openai)
        
        response = list(model.stream(messages, model="gpt-4"))
        
        mock_openai.chat.completions.create.assert_called_once_with(
            messages=messages,
            model="gpt-4",
            stream=True
        )
        assert response == [expected_response]
