# Memory / DB
import sqlite3
import json
from datetime import datetime
from typing import List, Dict, Optional, Tuple
from config import Config

class MemoryManager:
    """Memory manager for conversation persistence using SQLite"""
    
    def __init__(self):
        """Initialize database connection and create tables"""
        Config.ensure_directories()
        self.db_path = Config.DATABASE_PATH
        self.init_database()
    
    def init_database(self):
        """Initialize database tables"""
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Create conversations table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS conversations (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        session_id TEXT NOT NULL,
                        user_input TEXT NOT NULL,
                        bot_response TEXT NOT NULL,
                        timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
                        audio_file_path TEXT,
                        metadata TEXT
                    )
                ''')
                
                # Create sessions table
                cursor.execute('''
                    CREATE TABLE IF NOT EXISTS sessions (
                        session_id TEXT PRIMARY KEY,
                        created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
                        last_activity DATETIME DEFAULT CURRENT_TIMESTAMP,
                        title TEXT,
                        metadata TEXT
                    )
                ''')
                
                conn.commit()
                print("Database initialized successfully")
                
        except Exception as e:
            print(f"Error initializing database: {e}")
    
    def create_session(self, title: str = None) -> str:
        """
        Create a new conversation session
        
        Args:
            title: Optional session title
            
        Returns:
            Session ID
        """
        session_id = f"session_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        if not title:
            # Use English for better Windows compatibility
            title = f"Conversation {datetime.now().strftime('%Y-%m-%d %H:%M')}"
        
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO sessions (session_id, title)
                    VALUES (?, ?)
                ''', (session_id, title))
                conn.commit()
                
            print(f"New session created: {session_id}")
            return session_id
            
        except Exception as e:
            print(f"Error creating session: {e}")
            return session_id
    
    def save_conversation(self, session_id: str, user_input: str, bot_response: str, 
                         audio_file_path: str = None, metadata: Dict = None) -> bool:
        """
        Save conversation exchange to database
        
        Args:
            session_id: Session identifier
            user_input: User's input text
            bot_response: Bot's response text
            audio_file_path: Path to audio file (optional)
            metadata: Additional metadata (optional)
            
        Returns:
            True if successful, False otherwise
        """
        try:
            metadata_json = json.dumps(metadata) if metadata else None
            
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Save conversation
                cursor.execute('''
                    INSERT INTO conversations 
                    (session_id, user_input, bot_response, audio_file_path, metadata)
                    VALUES (?, ?, ?, ?, ?)
                ''', (session_id, user_input, bot_response, audio_file_path, metadata_json))
                
                # Update session last activity
                cursor.execute('''
                    UPDATE sessions 
                    SET last_activity = CURRENT_TIMESTAMP
                    WHERE session_id = ?
                ''', (session_id,))
                
                conn.commit()
                
            print(f"Conversation saved for session: {session_id}")
            return True
            
        except Exception as e:
            print(f"Error saving conversation: {e}")
            return False
    
    def get_conversation_history(self, session_id: str, limit: int = 20) -> List[Dict[str, str]]:
        """
        Get conversation history for a session
        
        Args:
            session_id: Session identifier
            limit: Maximum number of messages to retrieve
            
        Returns:
            List of conversation messages in format for LLM
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT user_input, bot_response, timestamp
                    FROM conversations
                    WHERE session_id = ?
                    ORDER BY timestamp ASC
                    LIMIT ?
                ''', (session_id, limit))
                
                rows = cursor.fetchall()
                
                # Convert to LLM message format
                messages = []
                for user_input, bot_response, timestamp in rows:
                    messages.append({
                        'role': 'user',
                        'content': user_input
                    })
                    messages.append({
                        'role': 'assistant',
                        'content': bot_response
                    })
                
                return messages
                
        except Exception as e:
            print(f"Error getting conversation history: {e}")
            return []
    
    def get_sessions(self, limit: int = 10) -> List[Tuple[str, str, str]]:
        """
        Get list of recent sessions
        
        Args:
            limit: Maximum number of sessions to retrieve
            
        Returns:
            List of tuples (session_id, title, last_activity)
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT session_id, title, last_activity
                    FROM sessions
                    ORDER BY last_activity DESC
                    LIMIT ?
                ''', (limit,))
                
                return cursor.fetchall()
                
        except Exception as e:
            print(f"Error getting sessions: {e}")
            return []
    
    def delete_session(self, session_id: str) -> bool:
        """
        Delete a conversation session and all its messages
        
        Args:
            session_id: Session identifier
            
        Returns:
            True if successful, False otherwise
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Delete conversations
                cursor.execute('DELETE FROM conversations WHERE session_id = ?', (session_id,))
                
                # Delete session
                cursor.execute('DELETE FROM sessions WHERE session_id = ?', (session_id,))
                
                conn.commit()
                
            print(f"Session deleted: {session_id}")
            return True
            
        except Exception as e:
            print(f"Error deleting session: {e}")
            return False
    
    def get_conversation_stats(self) -> Dict[str, int]:
        """
        Get statistics about conversations
        
        Returns:
            Dictionary with conversation statistics
        """
        try:
            with sqlite3.connect(self.db_path) as conn:
                cursor = conn.cursor()
                
                # Get total conversations
                cursor.execute('SELECT COUNT(*) FROM conversations')
                total_conversations = cursor.fetchone()[0]
                
                # Get total sessions
                cursor.execute('SELECT COUNT(*) FROM sessions')
                total_sessions = cursor.fetchone()[0]
                
                # Get conversations today
                cursor.execute('''
                    SELECT COUNT(*) FROM conversations 
                    WHERE DATE(timestamp) = DATE('now')
                ''')
                conversations_today = cursor.fetchone()[0]
                
                return {
                    'total_conversations': total_conversations,
                    'total_sessions': total_sessions,
                    'conversations_today': conversations_today
                }
                
        except Exception as e:
            print(f"Error getting conversation stats: {e}")
            return {
                'total_conversations': 0,
                'total_sessions': 0,
                'conversations_today': 0
            }