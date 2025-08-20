#!/usr/bin/env python3
"""
Test voice components for Super Kamen Bot
"""

def test_voice_components():
    print("🎤 Testing Voice Components...")
    print("=" * 40)
    
    # Test imports
    try:
        import whisper
        print("✅ Whisper package available")
    except ImportError:
        print("❌ Whisper not available")
        return False
    
    try:
        import sounddevice as sd
        import soundfile as sf
        print("✅ Audio packages available")
    except ImportError:
        print("❌ Audio packages not available")
        return False
    
    # Test Whisper model loading
    try:
        print("Loading Whisper model...")
        model = whisper.load_model("base")
        print("✅ Whisper model loaded successfully")
    except Exception as e:
        print(f"❌ Whisper model failed: {e}")
        return False
    
    # Test audio devices
    try:
        devices = sd.query_devices()
        print(f"✅ Found {len(devices)} audio devices")
        
        # Show microphone devices
        mics = [d for d in devices if d['max_input_channels'] > 0]
        print(f"✅ Found {len(mics)} microphone devices")
        
        if mics:
            print("📱 Available microphones:")
            for i, mic in enumerate(mics[:3]):  # Show first 3
                print(f"   {i+1}. {mic['name']}")
        
    except Exception as e:
        print(f"⚠️ Audio device check failed: {e}")
    
    # Test TTS
    try:
        from TTS.api import TTS
        print("✅ TTS package available")
    except ImportError:
        print("⚠️ TTS package not available (optional)")
    
    print("\n" + "=" * 40)
    print("🎉 Voice components test completed!")
    print("\n💡 If all ✅, voice features should work in the web app")
    print("🌐 Open: http://localhost:8503")
    
    return True

if __name__ == "__main__":
    test_voice_components()
