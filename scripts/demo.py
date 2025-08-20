#!/usr/bin/env python3
"""
Simple demo script for Super Kamen Bot
Demonstrates text-based Japanese conversation without web interface
"""

import sys
import os

# Add components to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'components'))

def demo_text_conversation():
    """Demonstrate text-based Japanese conversation"""
    print("🤖 Super Kamen Bot - Text Demo")
    print("=" * 40)
    print("日本語でお話しましょう！")
    print("Type 'quit' or 'exit' to end the conversation")
    print("-" * 40)
    
    try:
        from llm_handler import LLMHandler
        from memory_manager import MemoryManager
        
        # Initialize components
        print("Loading components...")
        llm = LLMHandler()
        memory = MemoryManager()
        
        # Ensure model is ready
        if not llm.ensure_model_ready():
            print("❌ Language model not available. Please check Ollama setup.")
            return
        
        # Create session
        session_id = memory.create_session("デモセッション")
        print(f"✅ Session created: {session_id}")
        print()
        
        # Conversation loop
        conversation_count = 0
        while True:
            try:
                # Get user input
                user_input = input("👤 あなた: ").strip()
                
                if user_input.lower() in ['quit', 'exit', 'やめる', '終了']:
                    print("👋 また会いましょう！")
                    break
                
                if not user_input:
                    continue
                
                # Get conversation history
                history = memory.get_conversation_history(session_id)
                
                # Generate response
                print("🤖 考え中...")
                response = llm.generate_response(user_input, history)
                
                if response:
                    print(f"🤖 ボット: {response}")
                    
                    # Save conversation
                    memory.save_conversation(session_id, user_input, response)
                    conversation_count += 1
                else:
                    print("❌ 応答の生成に失敗しました。")
                
                print()
                
            except KeyboardInterrupt:
                print("\n👋 さようなら！")
                break
            except Exception as e:
                print(f"❌ エラー: {e}")
        
        # Show stats
        if conversation_count > 0:
            print(f"\n📊 今回の会話数: {conversation_count}")
            stats = memory.get_conversation_stats()
            print(f"📊 総会話数: {stats['total_conversations']}")
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        print("💡 Please install requirements: pip install -r requirements.txt")
    except Exception as e:
        print(f"❌ Error: {e}")

def demo_ollama_test():
    """Test Ollama connection and model"""
    print("🧪 Testing Ollama Connection")
    print("-" * 30)
    
    try:
        import ollama
        
        # Test basic connection
        print("Testing Ollama connection...")
        response = ollama.chat(
            model='llama2:7b-chat',
            messages=[{'role': 'user', 'content': 'こんにちは'}]
        )
        
        print("✅ Ollama connection successful")
        print(f"Response: {response['message']['content']}")
        
        # List available models
        models = ollama.list()
        print(f"\nAvailable models:")
        for model in models.get('models', []):
            print(f"  - {model['name']}")
        
    except Exception as e:
        print(f"❌ Ollama test failed: {e}")
        print("💡 Make sure Ollama is running: ollama serve")

def main():
    """Main demo function"""
    print("🚀 Super Kamen Bot - Demo Mode")
    print("=" * 50)
    
    while True:
        print("\nChoose demo mode:")
        print("1. Text conversation demo")
        print("2. Ollama connection test")
        print("3. Exit")
        
        try:
            choice = input("\nEnter choice (1-3): ").strip()
            
            if choice == '1':
                demo_text_conversation()
            elif choice == '2':
                demo_ollama_test()
            elif choice == '3':
                print("👋 Goodbye!")
                break
            else:
                print("Invalid choice. Please enter 1, 2, or 3.")
                
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
