# 🔧 Super Kamen Bot - Troubleshooting Guide

## Quick Fix for Installation Issues

### ✅ **Step 1: Install Essential Packages Only**

Use the minimal requirements first:

```bash
# Windows users (recommended)
install-essential.bat

# Or manually
pip install -r requirements-minimal.txt
```

This installs only:
- `ollama` (LLM interface)
- `streamlit` (web interface)  
- `numpy`, `pandas` (data processing)
- `python-dotenv`, `requests` (utilities)

### ✅ **Step 2: Test Basic Functionality**

```bash
# Test Ollama connection
python quick_test.py

# Start web interface (text-only mode)
streamlit run main.py
```

### ✅ **Step 3: Add Audio Features (Optional)**

Only if you want voice capabilities:

```bash
# Install audio packages
pip install sounddevice soundfile

# Install Whisper for speech recognition  
pip install openai-whisper

# Install TTS (may have compatibility issues on some systems)
pip install TTS
```

## 🚨 Common Error Solutions

### Error: "No matching distribution found for sqlite3"
**Solution**: Remove `sqlite3` from requirements.txt (it's built into Python)
- ✅ **Fixed in latest version**

### Error: "Import 'streamlit' could not be resolved"
**Solution**: 
```bash
pip install streamlit
# or use
install-essential.bat
```

### Error: "Ollama connection failed"
**Solution**:
1. Install Ollama: https://ollama.ai/download
2. Start Ollama service: `ollama serve`
3. Pull a model: `ollama pull llama2:7b-chat`

### Error: TTS/Audio package installation fails
**Solution**: 
1. Use the app in text-only mode first
2. Audio features are optional and will be gracefully disabled
3. Try installing audio packages separately:
   ```bash
   pip install sounddevice soundfile
   pip install openai-whisper
   ```

### Error: Python version conflicts with TTS
**Solution**: 
- TTS package has strict Python version requirements
- Use text-only mode (works perfectly without TTS)
- Consider using Python 3.9 or 3.10 if TTS is essential

## 🎯 **Working Configurations**

### ✅ **Minimal Setup (Text-Only)**
- Python 3.8+
- Ollama running with any model
- Essential packages only
- **Features**: Text chat, conversation memory, web interface

### ✅ **Full Setup (Voice + Text)**  
- Python 3.9-3.10 (for TTS compatibility)
- Ollama with Japanese model
- All audio packages
- **Features**: Voice input/output, text chat, full functionality

## 🚀 **Quick Start Commands**

### Windows Users:
```batch
# Option 1: Essential only
install-essential.bat

# Option 2: Try full installation  
start.bat

# Option 3: Manual essential
pip install -r requirements-minimal.txt
streamlit run main.py
```

### Manual Steps:
```bash
# 1. Essential packages
pip install ollama streamlit numpy pandas

# 2. Start Ollama
ollama serve

# 3. Get a model
ollama pull llama2:7b-chat

# 4. Start the app
streamlit run main.py
```

## 💡 **Feature Availability**

| Feature | Essential Setup | Full Setup |
|---------|----------------|------------|
| Text chat | ✅ | ✅ |
| Conversation memory | ✅ | ✅ |
| Web interface | ✅ | ✅ |
| Japanese LLM | ✅ | ✅ |
| Voice input | ❌ | ✅ |
| Voice output | ❌ | ✅ |

## 🆘 **Still Having Issues?**

1. **Check system requirements**:
   ```bash
   python check_requirements.py
   ```

2. **Test individual components**:
   ```bash
   python quick_test.py  # Test Ollama
   python demo.py        # Test text chat
   ```

3. **Use minimal setup** and gradually add features

4. **Check Ollama status**:
   ```bash
   ollama list  # Should show available models
   ollama serve # Should start the service
   ```

The bot works perfectly in text-only mode with just the essential packages! 🎉
