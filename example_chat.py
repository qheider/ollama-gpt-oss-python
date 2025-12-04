#!/usr/bin/env python3
"""
Chat example: Interactive chat with GPT-OSS
"""
from ollama_client import OllamaClient


def main():
    # Initialize the client
    client = OllamaClient()
    
    print("=== Chat Completion Example ===\n")
    
    # Chat messages
    messages = [
        {
            "role": "system",
            "content": "You are a helpful AI assistant."
        },
        {
            "role": "user",
            "content": "What are the benefits of using open-source AI models?"
        }
    ]
    
    print("Chat History:")
    for msg in messages:
        print(f"{msg['role'].capitalize()}: {msg['content']}")
    
    print("\nAssistant:", end=" ", flush=True)
    
    # Send chat request
    response = client.chat(messages=messages)
    
    # Extract the assistant's message
    if "message" in response:
        print(response["message"].get("content", ""))
    elif "response" in response:
        print(response.get("response", ""))
    
    print("\n" + "="*50)


if __name__ == "__main__":
    main()
