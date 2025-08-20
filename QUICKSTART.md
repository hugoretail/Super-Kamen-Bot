# Super Kamen Bot - Quick Start Guide 🚀

## Immediate Setup (Windows)

1. **Double-click `start.bat`** - This will automatically:
   - Check if Python is installed
   - Check if Ollama is running
   - Install Python packages
   - Start the web interface

## Prerequisites Setup

### 1. Install Ollama
```bash
# Download from: https://ollama.ai/download
# After installation, start the service:
ollama serve
```

### 2. Install Japanese Language Model
```bash
# In a new terminal/command prompt:
ollama pull elyza/llama2-7b-chat
# or fallback:
ollama pull llama2:7b-chat
```

## Manual Start

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests (optional)
python test.py

# Start web interface
streamlit run main.py
```

## Usage

1. Open browser to: `http://localhost:8501`
2. Click "🎙️ 音声で話す" to use voice input
3. Or type in Japanese in the text area
4. Enjoy conversing in Japanese! 🇯🇵

## Troubleshooting

- **Ollama not found**: Install from https://ollama.ai/download
- **Model not found**: Run `ollama pull llama2:7b-chat`
- **Port in use**: Kill other Streamlit processes or use different port
- **Audio issues**: Check microphone permissions

## Next Steps

- Customize models in `config.py`
- Check conversation history in the sidebar
- Create new sessions for different topics
- View stats and manage past conversations

Happy chatting! 🤖✨
