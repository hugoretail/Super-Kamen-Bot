#!/usr/bin/env python3
"""
Quick Ollama test
"""

import ollama

def test_ollama():
    try:
        print("Testing Ollama connection...")
        response = ollama.chat(
            model='llama2:7b-chat',
            messages=[{'role': 'user', 'content': 'Say "Hello" in Japanese'}]
        )
        print("✅ Ollama working!")
        print("Response:", response['message']['content'])
        return True
    except Exception as e:
        print("❌ Ollama error:", e)
        return False

if __name__ == "__main__":
    test_ollama()
