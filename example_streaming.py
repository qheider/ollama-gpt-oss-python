#!/usr/bin/env python3
"""
Streaming example: Stream responses in real-time
"""
from ollama_client import OllamaClient


def main():
    # Initialize the client
    client = OllamaClient()
    
    print("=== Streaming Response Example ===\n")
    
    prompt = "Write a short story about AI and creativity (2-3 sentences)."
    
    print(f"Prompt: {prompt}\n")
    print("Response (streaming):")
    
    # Stream the response
    for chunk in client.generate_stream(prompt=prompt):
        print(chunk, end="", flush=True)
    
    print("\n" + "="*50)
    
    # Chat streaming example
    print("\n=== Streaming Chat Example ===\n")
    
    messages = [
        {
            "role": "user",
            "content": "Explain quantum computing in simple terms."
        }
    ]
    
    print("User: Explain quantum computing in simple terms.\n")
    print("Assistant: ", end="", flush=True)
    
    # Stream the chat response
    for chunk in client.chat_stream(messages=messages):
        print(chunk, end="", flush=True)
    
    print("\n" + "="*50)


if __name__ == "__main__":
    main()
