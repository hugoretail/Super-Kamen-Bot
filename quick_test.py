#!/usr/bin/env python3
"""
Quick Ollama test for Japanese model
"""

import ollama

def test_ollama():
    try:
        print("Testing Ollama connection with Japanese model...")
        response = ollama.chat(
            model='kangyufei/llama2:japanese',
            messages=[{'role': 'user', 'content': 'こんにちはと日本語で言ってください'}]
        )
        print("✅ Ollama working!")
        print("Response:", response['message']['content'])
        return True
    except Exception as e:
        print("❌ Ollama error:", e)
        print("💡 Make sure to pull the Japanese model first:")
        print("   ollama pull kangyufei/llama2:japanese")
        return False

if __name__ == "__main__":
    test_ollama()