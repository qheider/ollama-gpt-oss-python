"""
Simple tests for the Ollama client

These tests demonstrate the structure but require a running Ollama instance.
For actual testing, mock the requests or ensure Ollama is running.
"""
import unittest
from unittest.mock import patch, Mock
from ollama_client import OllamaClient


class TestOllamaClient(unittest.TestCase):
    """Test cases for OllamaClient"""
    
    def setUp(self):
        """Set up test client"""
        self.client = OllamaClient()
    
    def test_client_initialization(self):
        """Test client initialization with default values"""
        self.assertEqual(self.client.base_url, "http://localhost:11434")
        self.assertEqual(self.client.model, "gpt-oss")
    
    def test_client_initialization_custom(self):
        """Test client initialization with custom values"""
        client = OllamaClient(base_url="http://custom:8080", model="custom-model")
        self.assertEqual(client.base_url, "http://custom:8080")
        self.assertEqual(client.model, "custom-model")
    
    def test_base_url_trailing_slash(self):
        """Test that trailing slash is removed from base URL"""
        client = OllamaClient(base_url="http://localhost:11434/")
        self.assertEqual(client.base_url, "http://localhost:11434")
    
    @patch('ollama_client.requests.post')
    def test_generate(self, mock_post):
        """Test generate method"""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {"response": "Test response"}
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Call generate
        result = self.client.generate(prompt="Test prompt")
        
        # Verify
        self.assertEqual(result["response"], "Test response")
        mock_post.assert_called_once()
        
    @patch('ollama_client.requests.post')
    def test_chat(self, mock_post):
        """Test chat method"""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "message": {"role": "assistant", "content": "Test response"}
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Call chat
        messages = [{"role": "user", "content": "Hello"}]
        result = self.client.chat(messages=messages)
        
        # Verify
        self.assertEqual(result["message"]["content"], "Test response")
        mock_post.assert_called_once()
    
    @patch('ollama_client.requests.get')
    def test_list_models(self, mock_get):
        """Test list_models method"""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "models": [{"name": "gpt-oss"}, {"name": "llama2"}]
        }
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        # Call list_models
        result = self.client.list_models()
        
        # Verify
        self.assertEqual(len(result["models"]), 2)
        self.assertEqual(result["models"][0]["name"], "gpt-oss")
        mock_get.assert_called_once()
    
    @patch('ollama_client.requests.post')
    def test_model_info(self, mock_post):
        """Test model_info method"""
        # Mock response
        mock_response = Mock()
        mock_response.json.return_value = {
            "modelfile": "FROM gpt-oss",
            "parameters": "temperature 0.7"
        }
        mock_response.raise_for_status.return_value = None
        mock_post.return_value = mock_response
        
        # Call model_info
        result = self.client.model_info()
        
        # Verify
        self.assertEqual(result["modelfile"], "FROM gpt-oss")
        mock_post.assert_called_once()


if __name__ == "__main__":
    unittest.main()
