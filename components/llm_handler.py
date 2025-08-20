# TEXT GENERATION
# LLM Ollama (llama2:7b-chat)
import ollama
from typing import List, Dict, Optional
from config import Config

class LLMHandler:
    """LLM Handler using Ollama with Japanese-optimized model"""
    
    def __init__(self):
        """Initialize LLM handler"""
        self.model = Config.LLM_MODEL
        self.config = Config.get_ollama_config()
        print(f"LLM Handler initialized with model: {self.model}")
    
    def generate_response(self, user_input: str, conversation_history: List[Dict[str, str]] = None) -> Optional[str]:
        """
        Generate Japanese response using Ollama
        
        Args:
            user_input: User's input text in Japanese
            conversation_history: Previous conversation messages
            
        Returns:
            Generated Japanese response or None if error
        """
        try:
            # Prepare messages for conversation
            messages = []
            
            # Add system prompt
            messages.append({
                'role': 'system',
                'content': Config.SYSTEM_PROMPT
            })
            
            # Add conversation history if provided
            if conversation_history:
                for msg in conversation_history[-10:]:  # Keep last 10 messages for context
                    messages.append(msg)
            
            # Add current user input
            messages.append({
                'role': 'user',
                'content': user_input
            })
            
            print(f"Generating response for: {user_input}")
            
            # Generate response using Ollama
            response = ollama.chat(
                model=self.model,
                messages=messages,
                options={
                    'temperature': Config.LLM_TEMPERATURE,
                    'num_predict': Config.LLM_MAX_TOKENS,
                    'stop': ['<|endoftext|>', '\n\n\n'],  # Add stop sequences
                    'top_p': 0.9,  # Limit token diversity
                    'repeat_penalty': 1.1  # Reduce repetition
                }
            )
            
            generated_text = response['message']['content'].strip()
            
            # Clean up the response - remove any garbled text
            generated_text = self._clean_response(generated_text)
            
            print(f"Generated response: {generated_text}")
            return generated_text
            
        except Exception as e:
            print(f"Error generating response: {e}")
            return "申し訳ございませんが、エラーが発生しました。もう一度お試しください。"
    
    def _clean_response(self, text: str) -> str:
        """
        Clean up the generated response to remove garbled text
        
        Args:
            text: Raw response text
            
        Returns:
            Cleaned response text
        """
        import re
        
        # Remove sequences of numbers/random characters
        text = re.sub(r'\b\d{5,}\b', '', text)  # Remove long number sequences
        text = re.sub(r'[a-zA-Z]{10,}', '', text)  # Remove long English sequences
        text = re.sub(r'[^\u3040-\u309F\u30A0-\u30FF\u4E00-\u9FAF\u3000-\u303F\s。、！？「」（）]', '', text)  # Keep only Japanese chars and basic punctuation
        
        # Remove multiple spaces and clean up
        text = re.sub(r'\s+', ' ', text).strip()
        
        # If the text is too corrupted, return a fallback
        if len(text) < 10 or not any('\u3040' <= c <= '\u309F' or '\u30A0' <= c <= '\u30FF' or '\u4E00' <= c <= '\u9FAF' for c in text):
            return "申し訳ございませんが、適切な回答を生成できませんでした。もう一度お試しください。"
        
        return text
    
    def check_model_availability(self) -> bool:
        """
        Check if the required model is available in Ollama
        
        Returns:
            True if model is available, False otherwise
        """
        try:
            models = ollama.list()
            available_models = []
            
            # Handle different response formats
            if hasattr(models, 'models'):
                # New ollama version with object response
                for model in models.models:
                    if hasattr(model, 'name'):
                        available_models.append(model.name)
                    elif hasattr(model, 'model'):
                        available_models.append(model.model)
            elif isinstance(models, dict) and 'models' in models:
                # Dictionary response format
                for model in models['models']:
                    if isinstance(model, dict) and 'name' in model:
                        available_models.append(model['name'])
                    elif isinstance(model, dict) and 'model' in model:
                        available_models.append(model['model'])
            
            print(f"Available models: {available_models}")
            
            if self.model in available_models:
                print(f"Model {self.model} is available")
                return True
            else:
                print(f"Model {self.model} not found. Available models: {available_models}")
                return False
                
        except Exception as e:
            print(f"Error checking model availability: {e}")
            return False
    
    def pull_model(self) -> bool:
        """
        Download/pull the required model if not available
        
        Returns:
            True if successful, False otherwise
        """
        try:
            print(f"Pulling model: {self.model}")
            ollama.pull(self.model)
            print(f"Model {self.model} pulled successfully")
            return True
            
        except Exception as e:
            print(f"Error pulling model: {e}")
            return False
    
    def ensure_model_ready(self) -> bool:
        """
        Ensure the model is ready for use
        
        Returns:
            True if model is ready, False otherwise
        """
        if not self.check_model_availability():
            print(f"Model {self.model} not available, attempting to pull...")
            return self.pull_model()
        return True
