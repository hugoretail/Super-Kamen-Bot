#!/usr/bin/env python3
"""
List available Ollama models
"""

import ollama

def list_models():
    try:
        print("📋 Available Ollama models:")
        models = ollama.list()
        
        # Handle different response formats
        available_models = []
        if hasattr(models, 'models'):
            for model in models.models:
                if hasattr(model, 'name'):
                    available_models.append(model.name)
                elif hasattr(model, 'model'):
                    available_models.append(model.model)
        elif isinstance(models, dict) and 'models' in models:
            for model in models['models']:
                if isinstance(model, dict) and 'name' in model:
                    available_models.append(model['name'])
                elif isinstance(model, dict) and 'model' in model:
                    available_models.append(model['model'])
        
        if available_models:
            for i, model in enumerate(available_models, 1):
                print(f"  {i}. {model}")
        else:
            print("  No models found")
            
        # Check for Japanese model specifically
        japanese_model = "kangyufei/llama2:japanese"
        if japanese_model in available_models:
            print(f"\n✅ Japanese model '{japanese_model}' is available!")
        else:
            print(f"\n⚠️ Japanese model '{japanese_model}' not found")
            print(f"💡 Pull it with: ollama pull {japanese_model}")
            
    except Exception as e:
        print(f"❌ Error listing models: {e}")

if __name__ == "__main__":
    list_models()
