#!/usr/bin/env python3
"""
Model info example: Get information about available models
"""
from ollama_client import OllamaClient
import json


def main():
    # Initialize the client
    client = OllamaClient()
    
    print("=== Model Information Example ===\n")
    
    # List all available models
    print("Available Models:")
    print("-" * 50)
    
    try:
        models = client.list_models()
        if "models" in models:
            for model in models["models"]:
                print(f"  - {model.get('name', 'Unknown')}")
        else:
            print("  No models found or unable to retrieve model list")
    except Exception as e:
        print(f"  Error listing models: {e}")
    
    print("\n" + "="*50)
    
    # Get info about the default model
    print(f"\nInformation about '{client.model}':")
    print("-" * 50)
    
    try:
        info = client.model_info()
        # Print key information
        if "modelfile" in info:
            print(f"Modelfile:\n{info['modelfile'][:200]}...")
        if "parameters" in info:
            print(f"\nParameters: {info['parameters']}")
        if "template" in info:
            print(f"\nTemplate: {info['template'][:100]}...")
    except Exception as e:
        print(f"Error getting model info: {e}")
        print("\nNote: Make sure the 'gpt-oss' model is installed in Ollama")
        print("You can install it with: ollama pull gpt-oss")
    
    print("\n" + "="*50)


if __name__ == "__main__":
    main()
