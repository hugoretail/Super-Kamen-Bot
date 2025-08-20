# Super Kamen Bot 🤖

A Japanese conversational AI chatbot with voice capabilities, built with Streamlit, Ollama, and various AI models.

## Features ✨

- 🎤 **Voice Input**: Speech-to-text using OpenAI Whisper (Japanese optimized)
- 🧠 **Japanese AI**: Uses Japanese-optimized language models via Ollama
- 🔊 **Voice Output**: Text-to-speech using Coqui TTS for Japanese
- 💾 **Memory**: Persistent conversation history with SQLite database
- 🌐 **Web Interface**: Clean, responsive Streamlit web UI
- 🔄 **Session Management**: Create and switch between conversation sessions

## Quick Start 🚀

### Prerequisites

1. **Python 3.8+** - [Download Python](https://www.python.org/downloads/)
2. **Ollama** - [Download Ollama](https://ollama.ai/download)

### Automatic Setup

1. Clone or download this repository
2. Run the setup script:
   ```bash
   python setup.py
   ```
3. Follow the prompts to install dependencies and start the app

### Manual Setup

1. **Install Ollama and start the service:**
   ```bash
   # Download from https://ollama.ai/download
   ollama serve
   ```

2. **Install Python dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Pull the Japanese language model:**
   ```bash
   ollama pull elyza/llama2-7b-chat
   # or fallback to:
   ollama pull llama2:7b-chat
   ```

4. **Run tests to verify setup:**
   ```bash
   python test.py
   ```

5. **Start the web interface:**
   ```bash
   streamlit run main.py
   ```

## Usage 💬

### Web Interface

1. Open your browser to `http://localhost:8501`
2. Use the **voice input** by clicking "🎙️ 音声で話す" (Speak with Voice)
3. Or type your message in the **text input** area
4. View conversation history in the right panel
5. Manage sessions using the sidebar

### Voice Features

- **Recording**: Click the voice button and speak in Japanese
- **Transcription**: Automatic Japanese speech recognition
- **Response**: AI generates Japanese responses
- **Playback**: Automatic text-to-speech output

### Session Management

- **New Session**: Start fresh conversations
- **Session History**: View and load previous conversations
- **Persistent Memory**: All conversations are saved to SQLite database

## Architecture 🏗️

```
Super-Kamen-Bot/
├── main.py                 # Streamlit web application
├── config.py              # Configuration settings
├── test.py                # Component testing
├── setup.py               # Setup and installation
├── requirements.txt       # Python dependencies
├── components/
│   ├── speech_to_text.py  # Whisper STT (Japanese)
│   ├── llm_handler.py     # Ollama LLM interface
│   ├── text_to_speach.py  # Coqui TTS (Japanese)
│   └── memory_manager.py  # SQLite conversation storage
└── data/
    └── conversations.db   # SQLite database
```

## Configuration ⚙️

Edit `config.py` to customize:

- **Whisper Model**: STT accuracy vs speed
- **LLM Model**: Japanese language model selection
- **TTS Model**: Japanese voice selection
- **Audio Settings**: Sample rates, formats
- **Database**: Storage location

## Models Used 🤖

- **STT**: OpenAI Whisper (base/small) - Japanese forced
- **LLM**: elyza/llama2-7b-chat (Japanese optimized) or llama2:7b-chat
- **TTS**: Coqui TTS Japanese models (tts_models/ja/kokoro/tacotron2-DDC)

## Troubleshooting 🔧

### Common Issues

1. **Ollama not running**:
   ```bash
   ollama serve
   ```

2. **Model not found**:
   ```bash
   ollama pull elyza/llama2-7b-chat
   ```

3. **Audio issues**:
   - Check microphone permissions
   - Install audio drivers
   - Try different audio devices

4. **Import errors**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Port already in use**:
   ```bash
   streamlit run main.py --server.port 8502
   ```

### Logs and Debugging

- Check terminal output for error messages
- Run `python test.py` to diagnose component issues
- Verify Ollama models with `ollama list`

## Development 💻

### Adding Features

1. **New Components**: Add to `components/` directory
2. **Configuration**: Update `config.py`
3. **Testing**: Add tests to `test.py`
4. **UI**: Modify `main.py` Streamlit interface

### Database Schema

```sql
-- Sessions table
CREATE TABLE sessions (
    session_id TEXT PRIMARY KEY,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    last_activity DATETIME DEFAULT CURRENT_TIMESTAMP,
    title TEXT,
    metadata TEXT
);

-- Conversations table
CREATE TABLE conversations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_id TEXT NOT NULL,
    user_input TEXT NOT NULL,
    bot_response TEXT NOT NULL,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    audio_file_path TEXT,
    metadata TEXT
);
```

## Contributing 🤝

1. Fork the repository
2. Create a feature branch
3. Make changes with clear, English commit messages
4. Test your changes with `python test.py`
5. Submit a pull request

## License 📄

This project is open source. Feel free to use, modify, and distribute.

## Acknowledgments 🙏

- **Ollama** - Local LLM inference
- **OpenAI Whisper** - Speech recognition
- **Coqui TTS** - Text-to-speech synthesis
- **Streamlit** - Web interface framework
- **SQLite** - Lightweight database

---

**Super Kamen Bot** - Your Japanese conversation AI assistant! 🇯🇵🤖