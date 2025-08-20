# -*- coding: utf-8 -*-
# Configuration
import os
from typing import Dict, Any

# Set UTF-8 environment
os.environ['PYTHONIOENCODING'] = 'utf-8'

class Config:
    """Configuration for Super Kamen Bot - Japanese Conversational AI"""
    
    # Database settings
    DATABASE_PATH = "data/conversations.db"
    
    # Whisper STT settings
    WHISPER_MODEL = "base"  # or "small" for better accuracy
    WHISPER_LANGUAGE = "ja"  # Force Japanese
    
    # Ollama LLM settings
    LLM_MODEL = "kangyufei/llama2:japanese"  # Japanese-optimized model
    LLM_TEMPERATURE = 0.7
    LLM_MAX_TOKENS = 512
    
    # TTS settings
    TTS_MODEL = "tts_models/ja/kokoro/tacotron2-DDC"  # Japanese TTS model
    TTS_OUTPUT_PATH = "temp_audio"
    
    # Audio settings
    SAMPLE_RATE = 16000
    CHANNELS = 1
    CHUNK_SIZE = 1024
    AUDIO_FORMAT = "wav"
    
    # Streamlit settings
    WEB_PORT = 8501
    WEB_HOST = "localhost"
    
    # Japanese conversation prompts
    SYSTEM_PROMPT = """あなたは親切で知識豊富な日本語のアシスタントです。
常に自然で丁寧な日本語で回答してください。
日本の文化、習慣、言語について詳しく説明できます。
ユーザーとの会話を楽しく、教育的にしてください。"""
    
    @classmethod
    def get_ollama_config(cls) -> Dict[str, Any]:
        """Get Ollama configuration"""
        return {
            "model": cls.LLM_MODEL,
            "temperature": cls.LLM_TEMPERATURE,
            "max_tokens": cls.LLM_MAX_TOKENS,
            "system": cls.SYSTEM_PROMPT
        }
    
    @classmethod
    def ensure_directories(cls):
        """Ensure all required directories exist"""
        os.makedirs(os.path.dirname(cls.DATABASE_PATH), exist_ok=True)
        os.makedirs(cls.TTS_OUTPUT_PATH, exist_ok=True)