#!/usr/bin/env python3
"""
Requirements checker for Super Kamen Bot
Quick diagnosis of system requirements
"""

import sys
import subprocess
import importlib.util

def check_requirement(package_name, import_name=None):
    """Check if a package is installed"""
    if import_name is None:
        import_name = package_name
    
    try:
        importlib.import_module(import_name)
        print(f"✅ {package_name}")
        return True
    except ImportError:
        print(f"❌ {package_name} - Not installed")
        return False

def check_ollama():
    """Check Ollama availability"""
    try:
        result = subprocess.run(['ollama', '--version'], 
                              capture_output=True, text=True, timeout=5)
        if result.returncode == 0:
            print("✅ Ollama - Installed")
            
            # Check if running
            try:
                result = subprocess.run(['ollama', 'list'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    print("✅ Ollama - Running")
                    
                    # Check for models
                    if 'llama2' in result.stdout.lower():
                        print("✅ Ollama - Has language model")
                    else:
                        print("⚠️ Ollama - No language model found")
                        print("   Run: ollama pull llama2:7b-chat")
                    return True
                else:
                    print("❌ Ollama - Not running")
                    print("   Run: ollama serve")
                    return False
            except:
                print("❌ Ollama - Not responding")
                return False
        else:
            print("❌ Ollama - Installation issue")
            return False
    except FileNotFoundError:
        print("❌ Ollama - Not installed")
        print("   Download from: https://ollama.ai/download")
        return False
    except:
        print("❌ Ollama - Error checking")
        return False

def main():
    """Main requirements check"""
    print("🔍 Super Kamen Bot - Requirements Check")
    print("=" * 45)
    
    # Python version
    version = sys.version_info
    if version.major >= 3 and version.minor >= 8:
        print(f"✅ Python {version.major}.{version.minor}.{version.micro}")
    else:
        print(f"❌ Python {version.major}.{version.minor}.{version.micro} - Need 3.8+")
    
    print("\n📦 Core Dependencies:")
    
    # Check core packages
    core_packages = [
        ('ollama', 'ollama'),
        ('streamlit', 'streamlit'),
        ('sqlite3', 'sqlite3'),
        ('numpy', 'numpy'),
    ]
    
    core_ok = 0
    for package, import_name in core_packages:
        if check_requirement(package, import_name):
            core_ok += 1
    
    print("\n🎙️ Audio Dependencies:")
    
    # Check audio packages
    audio_packages = [
        ('openai-whisper', 'whisper'),
        ('sounddevice', 'sounddevice'),
        ('soundfile', 'soundfile'),
        ('TTS', 'TTS'),
    ]
    
    audio_ok = 0
    for package, import_name in audio_packages:
        if check_requirement(package, import_name):
            audio_ok += 1
    
    print("\n🤖 LLM Service:")
    ollama_ok = check_ollama()
    
    print("\n" + "=" * 45)
    print("📊 Summary:")
    print(f"Core packages: {core_ok}/{len(core_packages)}")
    print(f"Audio packages: {audio_ok}/{len(audio_packages)}")
    print(f"Ollama service: {'✅' if ollama_ok else '❌'}")
    
    if core_ok == len(core_packages) and ollama_ok:
        print("\n🎉 Ready to run Super Kamen Bot!")
        print("   Run: streamlit run main.py")
    elif core_ok == len(core_packages):
        print("\n⚠️ Core is ready, but Ollama needs setup")
        print("   1. Install Ollama: https://ollama.ai/download")
        print("   2. Run: ollama serve")
        print("   3. Run: ollama pull llama2:7b-chat")
    else:
        print("\n❌ Missing dependencies")
        print("   Run: pip install -r requirements.txt")
    
    if audio_ok < len(audio_packages):
        print("\n💡 Audio features may be limited")
        print("   Some voice features may not work")

if __name__ == "__main__":
    main()
