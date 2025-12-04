"""
Ollama GPT-OSS Client

A Python client for interacting with GPT-OSS models through Ollama.
"""
import json
import requests
from typing import Dict, List, Optional, Generator
from config import OLLAMA_BASE_URL, DEFAULT_MODEL, DEFAULT_TIMEOUT, DEFAULT_TEMPERATURE


class OllamaClient:
    """Client for interacting with Ollama API"""
    
    def __init__(self, base_url: str = OLLAMA_BASE_URL, model: str = DEFAULT_MODEL):
        """
        Initialize the Ollama client
        
        Args:
            base_url: The base URL for the Ollama API
            model: The model to use (default: gpt-oss)
        """
        self.base_url = base_url.rstrip('/')
        self.model = model
    
    def generate(
        self,
        prompt: str,
        temperature: float = DEFAULT_TEMPERATURE,
        max_tokens: Optional[int] = None,
        stream: bool = False,
        **kwargs
    ) -> Dict:
        """
        Generate a completion for the given prompt
        
        Args:
            prompt: The input prompt
            temperature: Controls randomness (0.0 to 1.0)
            max_tokens: Maximum number of tokens to generate
            stream: Whether to stream the response
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            The API response as a dictionary
        """
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": stream,
            **kwargs
        }
        
        if max_tokens:
            payload["options"] = payload.get("options", {})
            payload["options"]["num_predict"] = max_tokens
        
        response = requests.post(url, json=payload, timeout=DEFAULT_TIMEOUT, stream=stream)
        response.raise_for_status()
        
        if stream:
            return self._handle_stream(response)
        
        return response.json()
    
    def chat(
        self,
        messages: List[Dict[str, str]],
        temperature: float = DEFAULT_TEMPERATURE,
        stream: bool = False,
        **kwargs
    ) -> Dict:
        """
        Send a chat completion request
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Controls randomness (0.0 to 1.0)
            stream: Whether to stream the response
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            The API response as a dictionary
        """
        url = f"{self.base_url}/api/chat"
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": stream,
            **kwargs
        }
        
        response = requests.post(url, json=payload, timeout=DEFAULT_TIMEOUT, stream=stream)
        response.raise_for_status()
        
        if stream:
            return self._handle_stream(response)
        
        return response.json()
    
    def generate_stream(
        self,
        prompt: str,
        temperature: float = DEFAULT_TEMPERATURE,
        **kwargs
    ) -> Generator[str, None, None]:
        """
        Generate a streaming completion for the given prompt
        
        Args:
            prompt: The input prompt
            temperature: Controls randomness (0.0 to 1.0)
            **kwargs: Additional parameters to pass to the API
            
        Yields:
            Text chunks from the response
        """
        url = f"{self.base_url}/api/generate"
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "temperature": temperature,
            "stream": True,
            **kwargs
        }
        
        response = requests.post(url, json=payload, timeout=DEFAULT_TIMEOUT, stream=True)
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line)
                    if "response" in chunk:
                        yield chunk["response"]
                    if chunk.get("done", False):
                        break
                except json.JSONDecodeError:
                    # Skip malformed JSON lines
                    continue
    
    def chat_stream(
        self,
        messages: List[Dict[str, str]],
        temperature: float = DEFAULT_TEMPERATURE,
        **kwargs
    ) -> Generator[str, None, None]:
        """
        Send a streaming chat completion request
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Controls randomness (0.0 to 1.0)
            **kwargs: Additional parameters to pass to the API
            
        Yields:
            Text chunks from the response
        """
        url = f"{self.base_url}/api/chat"
        
        payload = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "stream": True,
            **kwargs
        }
        
        response = requests.post(url, json=payload, timeout=DEFAULT_TIMEOUT, stream=True)
        response.raise_for_status()
        
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line)
                    if "message" in chunk and "content" in chunk["message"]:
                        yield chunk["message"]["content"]
                    if chunk.get("done", False):
                        break
                except json.JSONDecodeError:
                    # Skip malformed JSON lines
                    continue
    
    def list_models(self) -> Dict:
        """
        List available models
        
        Returns:
            Dictionary containing list of available models
        """
        url = f"{self.base_url}/api/tags"
        response = requests.get(url, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        return response.json()
    
    def model_info(self, model: Optional[str] = None) -> Dict:
        """
        Get information about a specific model
        
        Args:
            model: The model name (defaults to the client's model)
            
        Returns:
            Model information dictionary
        """
        url = f"{self.base_url}/api/show"
        model_name = model or self.model
        
        payload = {"name": model_name}
        response = requests.post(url, json=payload, timeout=DEFAULT_TIMEOUT)
        response.raise_for_status()
        return response.json()
    
    def _handle_stream(self, response: requests.Response) -> Dict:
        """
        Handle streaming response and return the final result
        
        Args:
            response: The streaming response object
            
        Returns:
            The complete response as a dictionary
        """
        result = {}
        for line in response.iter_lines():
            if line:
                try:
                    chunk = json.loads(line)
                    result = chunk
                    if chunk.get("done", False):
                        break
                except json.JSONDecodeError:
                    # Skip malformed JSON lines
                    continue
        return result
