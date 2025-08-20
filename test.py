import ollama
import sys
import os

# Add components to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'components'))

def test_ollama_connection():
    """Test Ollama connection and Japanese model"""
    print("=== Testing Ollama Connection ===")
    
    try:
        # Test basic connection
        response = ollama.chat(model='llama2:7b-chat', messages=[
            {'role':'user','content':'Translate this in Japanese: "My cat is brown."'}
        ])
        
        print("✅ Ollama connection successful")
        print(f"Response: {response['message']['content']}")
        
        # Test Japanese model availability
        try:
            models = ollama.list()
            available_models = []
            
            # Handle different response formats
            if hasattr(models, 'models'):
                # New ollama version with object response
                for model in models.models:
                    if hasattr(model, 'name'):
                        available_models.append(model.name)
                    elif hasattr(model, 'model'):
                        available_models.append(model.model)
            elif isinstance(models, dict) and 'models' in models:
                # Dictionary response format
                for model in models['models']:
                    if isinstance(model, dict) and 'name' in model:
                        available_models.append(model['name'])
                    elif isinstance(model, dict) and 'model' in model:
                        available_models.append(model['model'])
            
            print(f"Available models: {available_models}")
        except Exception as model_error:
            print(f"⚠️ Could not list models: {model_error}")
            available_models = ["llama2:7b-chat"]  # Assume basic model
        
        # Check for Japanese optimized model
        target_model = "elyza/llama2-7b-chat"
        if target_model in available_models:
            print(f"✅ Japanese model {target_model} is available")
        else:
            print(f"⚠️ Japanese model {target_model} not found. Pulling...")
            try:
                ollama.pull(target_model)
                print(f"✅ Successfully pulled {target_model}")
            except Exception as e:
                print(f"❌ Failed to pull {target_model}: {e}")
                print("💡 Will use llama2:7b-chat as fallback")
        
    except Exception as e:
        print(f"❌ Ollama connection failed: {e}")
        print("💡 Make sure Ollama is running: ollama serve")
        return False
    
    return True

def test_components():
    """Test individual components"""
    print("\n=== Testing Components ===")
    
    try:
        # Test config
        from config import Config
        print("✅ Config loaded successfully")
        print(f"Database path: {Config.DATABASE_PATH}")
        print(f"Whisper language: {Config.WHISPER_LANGUAGE}")
        print(f"LLM model: {Config.LLM_MODEL}")
        
        # Test memory manager
        from memory_manager import MemoryManager
        memory = MemoryManager()
        print("✅ Memory manager initialized")
        
        # Create test session
        session_id = memory.create_session("テストセッション")
        print(f"✅ Test session created: {session_id}")
        
        # Test conversation saving
        success = memory.save_conversation(
            session_id,
            "こんにちは",
            "こんにちは！元気ですか？"
        )
        if success:
            print("✅ Conversation saved successfully")
        
        # Test conversation retrieval
        history = memory.get_conversation_history(session_id)
        if history:
            print(f"✅ Conversation history retrieved: {len(history)} messages")
        
        # Test LLM handler
        from llm_handler import LLMHandler
        llm = LLMHandler()
        print("✅ LLM handler initialized")
        
        if llm.check_model_availability():
            print("✅ LLM model is available")
            
            # Test response generation
            response = llm.generate_response("こんにちは、元気ですか？")
            if response:
                print(f"✅ LLM response generated: {response[:50]}...")
        else:
            print("⚠️ LLM model not available")
        
        # Test STT (only check if imports work)
        try:
            from speech_to_text import SpeechToText
            print("✅ Speech-to-text component loaded (requires audio packages)")
        except ImportError as e:
            print(f"⚠️ STT imports missing: {e}")
        
        # Test TTS (only check if imports work)
        try:
            from text_to_speach import TextToSpeech
            print("✅ Text-to-speech component loaded (requires TTS packages)")
        except ImportError as e:
            print(f"⚠️ TTS imports missing: {e}")
            
    except Exception as e:
        print(f"❌ Component test failed: {e}")
        return False
    
    return True

def test_japanese_conversation():
    """Test Japanese conversation flow"""
    print("\n=== Testing Japanese Conversation ===")
    
    try:
        from memory_manager import MemoryManager
        from llm_handler import LLMHandler
        
        memory = MemoryManager()
        llm = LLMHandler()
        
        # Create session
        session_id = memory.create_session("日本語テスト")
        
        # Test Japanese conversation
        test_inputs = [
            "おはようございます",
            "今日の天気はどうですか？",
            "日本の文化について教えてください",
            "ありがとうございました"
        ]
        
        for user_input in test_inputs:
            print(f"\n👤 User: {user_input}")
            
            # Get conversation history
            history = memory.get_conversation_history(session_id)
            
            # Generate response
            response = llm.generate_response(user_input, history)
            if response:
                print(f"🤖 Bot: {response}")
                
                # Save to memory
                memory.save_conversation(session_id, user_input, response)
            else:
                print("❌ Failed to generate response")
                return False
        
        print("\n✅ Japanese conversation test completed successfully")
        
        # Show stats
        stats = memory.get_conversation_stats()
        print(f"📊 Total conversations: {stats['total_conversations']}")
        
    except Exception as e:
        print(f"❌ Japanese conversation test failed: {e}")
        return False
    
    return True

def main():
    """Run all tests"""
    print("🚀 Super Kamen Bot - Component Testing")
    print("=" * 50)
    
    # Test Ollama connection
    if not test_ollama_connection():
        print("\n❌ Ollama test failed. Please ensure Ollama is running.")
        sys.exit(1)
    
    # Test components
    if not test_components():
        print("\n❌ Component test failed.")
        sys.exit(1)
    
    # Test Japanese conversation
    if not test_japanese_conversation():
        print("\n❌ Japanese conversation test failed.")
        sys.exit(1)
    
    print("\n" + "=" * 50)
    print("🎉 All tests passed! Super Kamen Bot is ready!")
    print("\n🚀 To start the web interface, run:")
    print("streamlit run main.py")

if __name__ == "__main__":
    main()