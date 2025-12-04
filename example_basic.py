#!/usr/bin/env python3
"""
Basic example: Simple text completion with GPT-OSS
"""
from ollama_client import OllamaClient


def main():
    # Initialize the client
    client = OllamaClient()
    
    print("=== Simple Text Completion Example ===\n")
    
    # Simple prompt
    prompt = "Explain what Ollama is in one sentence."
    
    print(f"Prompt: {prompt}\n")
    print("Response:")
    
    # Generate completion
    response = client.generate(prompt=prompt)
    
    print(response.get("response", ""))
    print("\n" + "="*50)


if __name__ == "__main__":
    main()
