# -*- coding: utf-8 -*-
import os
import sys

# Set UTF-8 environment variables first
os.environ['PYTHONIOENCODING'] = 'utf-8'
os.environ['LANG'] = 'en_US.UTF-8'
os.environ['LC_ALL'] = 'en_US.UTF-8'

import streamlit as st
import time
from datetime import datetime

# Set UTF-8 encoding for Windows
import locale
try:
    locale.setlocale(locale.LC_ALL, 'en_US.UTF-8')
except:
    try:
        locale.setlocale(locale.LC_ALL, 'C.UTF-8')
    except:
        pass  # Use system default

# Add components to path
sys.path.append(os.path.join(os.path.dirname(__file__), 'components'))

from speech_to_text import SpeechToText
from llm_handler import LLMHandler
from text_to_speach import TextToSpeech
from memory_manager import MemoryManager
from config import Config

class SuperKamenBot:
    """Main application class for Super Kamen Bot"""
    
    def __init__(self):
        """Initialize all components"""
        self.initialize_components()
    
    def initialize_components(self):
        """Initialize all bot components"""
        try:
            # Initialize components with error handling
            if 'stt' not in st.session_state:
                with st.spinner("音声認識モデルを読み込み中..."):
                    try:
                        st.session_state.stt = SpeechToText()
                        if not st.session_state.stt.available:
                            st.warning("音声認識が利用できません。テキストのみのモードで続行します。")
                    except Exception as e:
                        st.error(f"音声認識の初期化に失敗: {e}")
                        st.session_state.stt = None
            
            if 'llm' not in st.session_state:
                with st.spinner("言語モデルを読み込み中..."):
                    try:
                        st.session_state.llm = LLMHandler()
                        # Ensure model is ready
                        if not st.session_state.llm.ensure_model_ready():
                            st.error("言語モデルの準備ができませんでした。Ollamaが実行されているか確認してください。")
                            st.stop()
                    except Exception as e:
                        st.error(f"言語モデルの初期化に失敗: {e}")
                        st.stop()
            
            if 'tts' not in st.session_state:
                with st.spinner("音声合成モデルを読み込み中..."):
                    try:
                        st.session_state.tts = TextToSpeech()
                        if not st.session_state.tts.is_available():
                            st.warning("音声合成が利用できません。テキストのみのモードで続行します。")
                    except Exception as e:
                        st.warning(f"音声合成の初期化に失敗: {e}")
                        st.session_state.tts = None
            
            if 'memory' not in st.session_state:
                try:
                    st.session_state.memory = MemoryManager()
                except Exception as e:
                    st.error(f"メモリマネージャーの初期化に失敗: {e}")
                    st.stop()
            
            # Initialize session
            if 'current_session_id' not in st.session_state:
                st.session_state.current_session_id = st.session_state.memory.create_session()
            
            if 'conversation_history' not in st.session_state:
                st.session_state.conversation_history = []
            
            if 'audio_recording' not in st.session_state:
                st.session_state.audio_recording = False
            
            if 'show_text_input' not in st.session_state:
                st.session_state.show_text_input = False
                
        except Exception as e:
            st.error(f"初期化エラー: {e}")
            st.stop()
    
    def process_voice_input(self, duration: int = 5):
        """Process voice input and generate response"""
        if not st.session_state.stt or not st.session_state.stt.available:
            st.error("音声認識が利用できません。テキスト入力をご利用ください。")
            return
            
        try:
            # Record and transcribe
            with st.spinner(f"{duration}秒間録音中..."):
                user_text = st.session_state.stt.record_and_transcribe(duration)
            
            if not user_text:
                st.error("音声を認識できませんでした。もう一度お試しください。")
                return
            
            st.success(f"認識されたテキスト: {user_text}")
            
            # Generate response using the text processing method
            self.process_text_input(user_text)
                
        except Exception as e:
            st.error(f"音声処理エラー: {e}")
    
    def process_text_input(self, user_text: str):
        """Process text input and generate response"""
        try:
            if not user_text.strip():
                return
            
            # Generate response
            with st.spinner("応答を生成中..."):
                conversation_history = st.session_state.memory.get_conversation_history(
                    st.session_state.current_session_id
                )
                
                bot_response = st.session_state.llm.generate_response(
                    user_text, 
                    conversation_history
                )
            
            if bot_response:
                # Save to memory
                st.session_state.memory.save_conversation(
                    st.session_state.current_session_id,
                    user_text,
                    bot_response
                )
                
                # Add to session conversation history
                st.session_state.conversation_history.append({
                    'user': user_text,
                    'bot': bot_response,
                    'timestamp': datetime.now()
                })
                
                # Generate speech if available
                if st.session_state.tts and st.session_state.tts.is_available():
                    with st.spinner("音声を生成中..."):
                        success = st.session_state.tts.text_to_speech_play(bot_response)
                        if not success:
                            st.warning("音声再生に失敗しました。")
                
        except Exception as e:
            st.error(f"テキスト処理エラー: {e}")

def main():
    """Main Streamlit application"""
    
    # Page configuration
    st.set_page_config(
        page_title="Super Kamen Bot",
        page_icon="🤖",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS - Instagram/Skype-style conversation
    st.markdown("""
    <style>
    .main-header {
        text-align: center;
        padding: 1rem 0;
        background: linear-gradient(90deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-size: 3rem;
        font-weight: bold;
    }
    
    /* Chat container like messaging apps */
    .chat-container {
        max-height: 400px;
        overflow-y: auto;
        padding: 1rem;
        background: #f8f9fa;
        border-radius: 15px;
        margin: 1rem 0;
        border: 1px solid #e9ecef;
    }
    
    /* User messages - right aligned like you send */
    .user-message {
        background: linear-gradient(135deg, #007bff, #0056b3);
        color: white;
        padding: 0.8rem 1.2rem;
        border-radius: 18px 18px 5px 18px;
        margin: 0.3rem 0 0.3rem auto;
        max-width: 75%;
        word-wrap: break-word;
        text-align: left;
        display: block;
        float: right;
        clear: both;
    }
    
    /* Bot messages - left aligned like you receive */
    .bot-message {
        background: #e9ecef;
        color: #333;
        padding: 0.8rem 1.2rem;
        border-radius: 18px 18px 18px 5px;
        margin: 0.3rem auto 0.3rem 0;
        max-width: 75%;
        word-wrap: break-word;
        border: 1px solid #dee2e6;
        display: block;
        float: left;
        clear: both;
    }
    
    .clearfix::after {
        content: "";
        display: table;
        clear: both;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Header
    st.markdown('<h1 class="main-header">Super Kamen Bot 🤖</h1>', unsafe_allow_html=True)
    st.markdown('<p style="text-align: center; font-size: 1.2rem; color: #666;">日本語会話AI アシスタント</p>', unsafe_allow_html=True)
    
    # Initialize bot
    bot = SuperKamenBot()
    
    # Sidebar
    with st.sidebar:
        st.header("🎛️ コントロール")
        
        # Session management
        st.subheader("セッション管理")
        
        # New session button
        if st.button("🆕 新しい会話を開始"):
            st.session_state.current_session_id = st.session_state.memory.create_session()
            st.session_state.conversation_history = []
            st.success("新しい会話を開始しました！")
            st.rerun()
        
        # Session stats
        stats = st.session_state.memory.get_conversation_stats()
        st.metric("総会話数", stats['total_conversations'])
        st.metric("今日の会話数", stats['conversations_today'])
        
        # Recent sessions
        st.subheader("最近のセッション")
        sessions = st.session_state.memory.get_sessions(5)
        for session_id, title, last_activity in sessions:
            if st.button(f"📋 {title}", key=f"session_{session_id}"):
                st.session_state.current_session_id = session_id
                st.session_state.conversation_history = []
                # Load conversation history for display
                history = st.session_state.memory.get_conversation_history(session_id, 50)
                display_history = []
                for i in range(0, len(history), 2):
                    if i + 1 < len(history):
                        display_history.append({
                            'user': history[i]['content'],
                            'bot': history[i + 1]['content'],
                            'timestamp': datetime.now()  # Placeholder
                        })
                st.session_state.conversation_history = display_history
                st.success(f"セッション '{title}' を読み込みました")
                st.rerun()
    
    # Main content area - single column clean layout
    
    # Voice input (prominent)
    if st.session_state.stt and st.session_state.stt.available:
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            if st.button("� 音声で話す", type="primary", use_container_width=True):
                bot.process_voice_input(5)
    else:
        st.info("💡 音声入力は利用できません。")
    
    # Text input toggle (small button)
    col1, col2, col3, col4, col5 = st.columns([2, 1, 1, 1, 2])
    with col3:
        if st.button("💬", help="テキスト入力を表示/非表示"):
            st.session_state.show_text_input = not st.session_state.show_text_input
    
    # Text input (hidden by default)
    if st.session_state.show_text_input:
        with st.form("text_form", clear_on_submit=True):
            user_input = st.text_input("", placeholder="日本語でメッセージを入力してください...")
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                if st.form_submit_button("送信", use_container_width=True):
                    if user_input:
                        bot.process_text_input(user_input)
                        st.rerun()
    
    # Chat history - Instagram/Skype style
    st.markdown('<div class="chat-container">', unsafe_allow_html=True)
    
    if st.session_state.conversation_history:
        # Show messages in chronological order (oldest to newest like real chat)
        for exchange in st.session_state.conversation_history[-10:]:  # Last 10 messages
            # User message (right side like you send)
            st.markdown(f"""
            <div class="user-message">
                {exchange['user']}
            </div>
            <div class="clearfix"></div>
            """, unsafe_allow_html=True)
            
            # Bot message (left side like you receive)
            st.markdown(f"""
            <div class="bot-message">
                {exchange['bot']}
            </div>
            <div class="clearfix"></div>
            """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="text-align: center; color: #888; padding: 2rem;">
            <p>🎯 音声ボタンを押して会話を始めましょう！</p>
        </div>
        """, unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #888;">Super Kamen Bot - 日本語会話AI © 2025</p>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()