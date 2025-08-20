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
    LLM_TEMPERATURE = 0.3  # Lower temperature for more consistent output
    LLM_MAX_TOKENS = 256   # Reduced for more focused responses
    
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
以下のルールに従って回答してください：
1. 常に正しい日本語のみで回答する
2. 英語や数字の羅列は使わない
3. 簡潔で自然な会話を心がける
4. 丁寧語を使用する
5. ユーザーの質問に直接答える
6. 文字化けや意味不明な文字は絶対に出力しない

日本の文化、習慣、言語について質問された場合は、正確で分かりやすい情報を提供してください。"""
    
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