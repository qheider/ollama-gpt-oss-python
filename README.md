# ollama-gpt-oss-python

This is a project to explore how to use a free model (gpt-oss) internally using Ollama.

## Overview

This Python client provides a simple and intuitive interface for interacting with GPT-OSS and other open-source models through Ollama. It supports text completion, chat-based interactions, and streaming responses.

## Features

- ✨ Simple API for text completion and chat
- 🔄 Streaming response support
- ⚙️ Configurable via environment variables
- 📝 Multiple example scripts demonstrating different use cases
- 🎯 Type hints for better IDE support

## Prerequisites

- Python 3.7 or higher
- [Ollama](https://ollama.ai/) installed and running
- GPT-OSS model (or any other Ollama-compatible model)

### Installing Ollama

1. Download and install Ollama from [https://ollama.ai/](https://ollama.ai/)
2. Pull the GPT-OSS model (or another model of your choice):
   ```bash
   ollama pull gpt-oss
   ```
3. Verify Ollama is running:
   ```bash
   ollama list
   ```

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/qheider/ollama-gpt-oss-python.git
   cd ollama-gpt-oss-python
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. (Optional) Configure environment variables:
   ```bash
   cp .env.example .env
   # Edit .env with your preferred settings
   ```

## Usage

### Basic Text Completion

```python
from ollama_client import OllamaClient

client = OllamaClient()
response = client.generate(prompt="Explain what Ollama is in one sentence.")
print(response.get("response", ""))
```

Run the example:
```bash
python example_basic.py
```

### Chat Completion

```python
from ollama_client import OllamaClient

client = OllamaClient()
messages = [
    {"role": "system", "content": "You are a helpful AI assistant."},
    {"role": "user", "content": "What are the benefits of using open-source AI models?"}
]
response = client.chat(messages=messages)
print(response["message"]["content"])
```

Run the example:
```bash
python example_chat.py
```

### Streaming Responses

```python
from ollama_client import OllamaClient

client = OllamaClient()
for chunk in client.generate_stream(prompt="Write a short story about AI."):
    print(chunk, end="", flush=True)
```

Run the example:
```bash
python example_streaming.py
```

### Model Information

```python
from ollama_client import OllamaClient

client = OllamaClient()
models = client.list_models()
info = client.model_info()
```

Run the example:
```bash
python example_model_info.py
```

## Configuration

You can configure the client using environment variables in a `.env` file:

| Variable | Default | Description |
|----------|---------|-------------|
| `OLLAMA_BASE_URL` | `http://localhost:11434` | The URL where Ollama is running |
| `DEFAULT_MODEL` | `gpt-oss` | The default model to use |
| `DEFAULT_TIMEOUT` | `60` | Request timeout in seconds |
| `DEFAULT_TEMPERATURE` | `0.7` | Default temperature for generation (0.0-1.0) |

## API Reference

### OllamaClient

#### `__init__(base_url, model)`
Initialize the Ollama client.

#### `generate(prompt, temperature, max_tokens, stream, **kwargs)`
Generate a completion for the given prompt.

#### `chat(messages, temperature, stream, **kwargs)`
Send a chat completion request.

#### `generate_stream(prompt, temperature, **kwargs)`
Generate a streaming completion (yields text chunks).

#### `chat_stream(messages, temperature, **kwargs)`
Send a streaming chat request (yields text chunks).

#### `list_models()`
List all available models.

#### `model_info(model)`
Get information about a specific model.

## Examples

The repository includes several example scripts:

- `example_basic.py` - Simple text completion
- `example_chat.py` - Chat-based interaction
- `example_streaming.py` - Streaming responses
- `example_model_info.py` - Model information retrieval

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is open source and available under the MIT License.

## Resources

- [Ollama Documentation](https://github.com/ollama/ollama)
- [Ollama API Reference](https://github.com/ollama/ollama/blob/main/docs/api.md)
- [GPT-OSS Model Information](https://ollama.ai/library/gpt-oss)
