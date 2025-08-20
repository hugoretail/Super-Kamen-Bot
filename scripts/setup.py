#!/usr/bin/env python3
"""
Setup script for Super Kamen Bot
Helps with installation and configuration
"""

import os
import sys
import subprocess
import platform

def check_python_version():
    """Check if Python version is suitable"""
    version = sys.version_info
    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("❌ Python 3.8 or higher is required")
        print(f"Current version: {version.major}.{version.minor}.{version.micro}")
        return False
    
    print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
    return True

def check_ollama():
    """Check if Ollama is installed and running"""
    try:
        result = subprocess.run(['ollama', '--version'], 
                              capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            print("✅ Ollama is installed")
            
            # Check if Ollama is running
            try:
                result = subprocess.run(['ollama', 'list'], 
                                      capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    print("✅ Ollama is running")
                    return True
                else:
                    print("⚠️ Ollama is installed but not running")
                    print("💡 Start Ollama with: ollama serve")
                    return False
            except subprocess.TimeoutExpired:
                print("⚠️ Ollama is not responding")
                return False
                
    except FileNotFoundError:
        print("❌ Ollama is not installed")
        print("💡 Install from: https://ollama.ai/download")
        return False
    except subprocess.TimeoutExpired:
        print("❌ Ollama check timed out")
        return False

def install_requirements():
    """Install Python requirements"""
    print("\n📦 Installing Python requirements...")
    
    try:
        subprocess.run([sys.executable, '-m', 'pip', 'install', '-r', 'requirements.txt'], 
                      check=True)
        print("✅ Requirements installed successfully")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Failed to install requirements: {e}")
        return False

def setup_ollama_model():
    """Setup Japanese-optimized Ollama model"""
    print("\n🤖 Setting up Japanese language model...")
    
    models_to_try = [
        "elyza/llama2-7b-chat",  # Japanese-optimized
        "llama2:7b-chat"         # Fallback
    ]
    
    for model in models_to_try:
        try:
            print(f"Checking model: {model}")
            result = subprocess.run(['ollama', 'show', model], 
                                  capture_output=True, text=True, timeout=30)
            
            if result.returncode == 0:
                print(f"✅ Model {model} is available")
                return model
            else:
                print(f"⚠️ Model {model} not found, pulling...")
                result = subprocess.run(['ollama', 'pull', model], 
                                      timeout=600)  # 10 minutes timeout
                if result.returncode == 0:
                    print(f"✅ Model {model} pulled successfully")
                    return model
                else:
                    print(f"❌ Failed to pull {model}")
                    
        except subprocess.TimeoutExpired:
            print(f"⏰ Timeout pulling {model}")
        except Exception as e:
            print(f"❌ Error with {model}: {e}")
    
    print("❌ Failed to setup any model")
    return None

def create_directories():
    """Create necessary directories"""
    print("\n📁 Creating directories...")
    
    directories = [
        "data",
        "temp_audio"
    ]
    
    for directory in directories:
        os.makedirs(directory, exist_ok=True)
        print(f"✅ Directory created: {directory}")

def run_tests():
    """Run component tests"""
    print("\n🧪 Running tests...")
    
    try:
        result = subprocess.run([sys.executable, 'test.py'], timeout=120)
        if result.returncode == 0:
            print("✅ All tests passed")
            return True
        else:
            print("❌ Some tests failed")
            return False
    except subprocess.TimeoutExpired:
        print("⏰ Tests timed out")
        return False
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False

def start_web_app():
    """Start the Streamlit web application"""
    print("\n🚀 Starting Super Kamen Bot web interface...")
    print("💡 The app will open in your browser")
    print("💡 Press Ctrl+C to stop the application")
    
    try:
        subprocess.run([sys.executable, '-m', 'streamlit', 'run', 'main.py'])
    except KeyboardInterrupt:
        print("\n👋 Super Kamen Bot stopped")
    except Exception as e:
        print(f"❌ Error starting web app: {e}")

def main():
    """Main setup function"""
    print("🚀 Super Kamen Bot Setup")
    print("=" * 50)
    
    # Check Python version
    if not check_python_version():
        sys.exit(1)
    
    # Check Ollama
    ollama_ok = check_ollama()
    
    # Install requirements
    if not install_requirements():
        print("❌ Setup failed: Could not install requirements")
        sys.exit(1)
    
    # Create directories
    create_directories()
    
    # Setup Ollama model if Ollama is available
    if ollama_ok:
        model = setup_ollama_model()
        if not model:
            print("⚠️ No language model available, but continuing...")
    else:
        print("⚠️ Ollama not available, skipping model setup")
    
    # Run tests
    if ollama_ok:
        test_success = run_tests()
        if not test_success:
            print("⚠️ Some tests failed, but continuing...")
    
    print("\n" + "=" * 50)
    print("🎉 Setup completed!")
    print("\n📋 Next steps:")
    
    if not ollama_ok:
        print("1. Install and start Ollama: https://ollama.ai/download")
        print("2. Run: ollama serve")
        print("3. Re-run this setup script")
    else:
        print("1. Start the web interface with: streamlit run main.py")
        print("2. Or run this script again to auto-start")
    
    # Ask if user wants to start the web app
    if ollama_ok:
        try:
            answer = input("\n🚀 Start the web interface now? (y/N): ").strip().lower()
            if answer in ['y', 'yes']:
                start_web_app()
        except KeyboardInterrupt:
            print("\n👋 Goodbye!")

if __name__ == "__main__":
    main()
