import streamlit as st
import os
import sys
import time
from datetime import datetime

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
            # Initialize components
            if 'stt' not in st.session_state:
                with st.spinner("音声認識モデルを読み込み中..."):
                    st.session_state.stt = SpeechToText()
            
            if 'llm' not in st.session_state:
                with st.spinner("言語モデルを読み込み中..."):
                    st.session_state.llm = LLMHandler()
                    # Ensure model is ready
                    if not st.session_state.llm.ensure_model_ready():
                        st.error("言語モデルの準備ができませんでした。Ollamaが実行されているか確認してください。")
                        st.stop()
            
            if 'tts' not in st.session_state:
                with st.spinner("音声合成モデルを読み込み中..."):
                    st.session_state.tts = TextToSpeech()
                    if not st.session_state.tts.is_available():
                        st.warning("音声合成が利用できません。テキストのみのモードで続行します。")
            
            if 'memory' not in st.session_state:
                st.session_state.memory = MemoryManager()
            
            # Initialize session
            if 'current_session_id' not in st.session_state:
                st.session_state.current_session_id = st.session_state.memory.create_session()
            
            if 'conversation_history' not in st.session_state:
                st.session_state.conversation_history = []
            
            if 'audio_recording' not in st.session_state:
                st.session_state.audio_recording = False
                
        except Exception as e:
            st.error(f"初期化エラー: {e}")
            st.stop()
    
    def process_voice_input(self, duration: int = 5):
        """Process voice input and generate response"""
        try:
            # Record and transcribe
            with st.spinner(f"{duration}秒間録音中..."):
                user_text = st.session_state.stt.record_and_transcribe(duration)
            
            if not user_text:
                st.error("音声を認識できませんでした。もう一度お試しください。")
                return
            
            st.success(f"認識されたテキスト: {user_text}")
            
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
                
                # Display response
                st.write("**ボットの応答:**")
                st.write(bot_response)
                
                # Generate speech
                if st.session_state.tts.is_available():
                    with st.spinner("音声を生成中..."):
                        success = st.session_state.tts.text_to_speech_play(bot_response)
                        if not success:
                            st.warning("音声再生に失敗しました。")
                
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
                if st.session_state.tts.is_available():
                    with st.spinner("音声を生成中..."):
                        st.session_state.tts.text_to_speech_play(bot_response)
                
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
    
    # Custom CSS
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
    .chat-message {
        padding: 1rem;
        margin: 0.5rem 0;
        border-radius: 10px;
    }
    .user-message {
        background-color: #E3F2FD;
        border-left: 4px solid #2196F3;
    }
    .bot-message {
        background-color: #F3E5F5;
        border-left: 4px solid #9C27B0;
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
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.header("💬 会話")
        
        # Voice input section
        st.subheader("🎤 音声入力")
        
        col_voice1, col_voice2 = st.columns([1, 1])
        
        with col_voice1:
            duration = st.slider("録音時間 (秒)", min_value=3, max_value=10, value=5)
        
        with col_voice2:
            if st.button("🎙️ 音声で話す", type="primary", use_container_width=True):
                bot.process_voice_input(duration)
        
        st.divider()
        
        # Text input section
        st.subheader("⌨️ テキスト入力")
        
        # Text input form
        with st.form("text_input_form", clear_on_submit=True):
            user_input = st.text_area(
                "メッセージを入力してください:",
                height=100,
                placeholder="日本語でメッセージを入力してください..."
            )
            submit_button = st.form_submit_button("💬 送信", type="primary", use_container_width=True)
            
            if submit_button and user_input:
                bot.process_text_input(user_input)
                st.rerun()
    
    with col2:
        st.header("📝 会話履歴")
        
        # Display conversation history
        if st.session_state.conversation_history:
            for i, exchange in enumerate(reversed(st.session_state.conversation_history[-10:])):
                # User message
                st.markdown(f"""
                <div class="chat-message user-message">
                    <strong>👤 あなた:</strong><br>
                    {exchange['user']}
                </div>
                """, unsafe_allow_html=True)
                
                # Bot message
                st.markdown(f"""
                <div class="chat-message bot-message">
                    <strong>🤖 ボット:</strong><br>
                    {exchange['bot']}
                </div>
                """, unsafe_allow_html=True)
                
                if i < len(st.session_state.conversation_history) - 1:
                    st.markdown("---")
        else:
            st.info("まだ会話がありません。音声またはテキストで話しかけてください！")
    
    # Footer
    st.markdown("---")
    st.markdown(
        '<p style="text-align: center; color: #888;">Super Kamen Bot - 日本語会話AI © 2025</p>',
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    main()