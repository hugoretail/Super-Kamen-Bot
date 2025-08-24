# 🤖 Super Kamen Bot

A Japanese conversational AI chatbot with voice interaction capabilities, built for language learning and practice.

![Python](https://img.shields.io/badge/python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/streamlit-web%20app-red.svg)
![Japanese](https://img.shields.io/badge/language-Japanese-green.svg)

## 🌟 Features

🎤 **Voice Interaction**
- Speech-to-text with Japanese language optimization
- Voice activity detection (automatic recording stop)
- Real-time audio processing

🧠 **Japanese AI Chat**
- Japanese-optimized LLM (kangyufei/llama2:japanese)
- Natural conversation flow
- Context-aware responses

💾 **Persistent Memory**
- SQLite conversation storage
- Session management
- Chat history across sessions

🌐 **Modern Web Interface**
- Clean, Instagram/Skype-style chat design
- Voice-first interaction
- Responsive design

## 🏗️ Project Structure

```
Super-Kamen-Bot/
├── main.py                    # Streamlit web application
├── config.py                  # Configuration settings
├── requirements.txt           # Dependencies
├── components/
│   ├── speech_to_text.py     # Voice recognition (Whisper)
│   ├── llm_handler.py        # LLM interface (Ollama)
│   ├── text_to_speach.py     # Text-to-speech
│   └── memory_manager.py     # Database management
└── data/
    └── conversations.db       # SQLite database
```

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- [Ollama](https://ollama.ai/) installed and running
- Microphone access

### Installation

```bash
# Clone the repository
git clone <repository-url>
cd Super-Kamen-Bot

# Install dependencies
pip install -r requirements.txt

# Pull the Japanese AI model
ollama pull kangyufei/llama2:japanese

# Start Ollama service
ollama serve
```

### Run the Application

```bash
# Windows (UTF-8 support)
start-utf8.bat

# Or manual start
streamlit run main.py
```

Open http://localhost:8501 in your browser.

## 🎯 Usage

1. **Click the voice button (🎤)** to start speaking in Japanese
2. **Speak naturally** - recording stops automatically when you pause
3. **View the conversation** in the chat interface
4. **Optional text input** - click 💬 to toggle text mode

## 🔧 Configuration

Edit `config.py` to customize:
- Model settings
- Audio parameters
- UI preferences

## 📋 Requirements

**Core:**
- ollama>=0.1.0
- streamlit>=1.28.0
- openai-whisper>=20231117

**Optional (for full features):**
- TTS>=0.22.0 (voice output)
- sounddevice>=0.4.6 (audio recording)

## 🌍 Language Support

Optimized for Japanese conversation:
- Japanese speech recognition
- Japanese text generation
- Japanese UI elements

## 📄 License

MIT License - feel free to use and modify!

---

**Happy chatting in Japanese! 🇯🇵**