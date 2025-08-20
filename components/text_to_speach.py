# TTS
# Coqui
import os
import tempfile
from typing import Optional

# Try to import audio packages, handle gracefully if missing
try:
    import sounddevice as sd
    import soundfile as sf
    AUDIO_AVAILABLE = True
except ImportError:
    print("⚠️ Audio packages not available. Audio playback will be disabled.")
    print("💡 Install with: pip install sounddevice soundfile")
    AUDIO_AVAILABLE = False
    sd = None
    sf = None

from config import Config

class TextToSpeech:
    """Text-to-Speech using Coqui TTS for Japanese"""
    
    def __init__(self):
        """Initialize TTS model for Japanese"""
        self.tts = None
        self.tts_available = False
        
        try:
            print("Loading Japanese TTS model...")
            # Initialize TTS with Japanese model
            from TTS.api import TTS
            self.tts = TTS(model_name=Config.TTS_MODEL)
            self.tts_available = True
            print(f"TTS model loaded: {Config.TTS_MODEL}")
            
        except ImportError:
            print("⚠️ TTS package not installed. Text-to-speech will be disabled.")
            print("💡 Install with: pip install TTS")
            
        except Exception as e:
            print(f"⚠️ TTS initialization failed: {e}")
            print("💡 Text-to-speech will be disabled.")
            
        finally:
            # Ensure output directory exists
            Config.ensure_directories()
    
    def text_to_speech_file(self, text: str, output_path: str = None) -> Optional[str]:
        """
        Convert Japanese text to speech and save to file
        
        Args:
            text: Japanese text to convert
            output_path: Output file path (if None, creates temporary file)
            
        Returns:
            Path to generated audio file or None if error
        """
        if not self.tts:
            print("TTS model not available")
            return None
        
        try:
            if not output_path:
                # Create temporary file
                temp_file = tempfile.NamedTemporaryFile(
                    suffix=".wav", 
                    dir=Config.TTS_OUTPUT_PATH,
                    delete=False
                )
                output_path = temp_file.name
                temp_file.close()
            
            print(f"Converting text to speech: {text}")
            
            # Generate speech
            self.tts.tts_to_file(
                text=text,
                file_path=output_path
            )
            
            print(f"Audio saved to: {output_path}")
            return output_path
            
        except Exception as e:
            print(f"Error during TTS conversion: {e}")
            return None
    
    def text_to_speech_play(self, text: str) -> bool:
        """
        Convert Japanese text to speech and play immediately
        
        Args:
            text: Japanese text to convert and play
            
        Returns:
            True if successful, False otherwise
        """
        audio_file = self.text_to_speech_file(text)
        if audio_file:
            success = self.play_audio_file(audio_file)
            # Clean up temporary file
            try:
                os.unlink(audio_file)
            except Exception as e:
                print(f"Warning: Could not delete temporary file {audio_file}: {e}")
            return success
        return False
    
    def play_audio_file(self, audio_file_path: str) -> bool:
        """
        Play audio file using sounddevice
        
        Args:
            audio_file_path: Path to audio file
            
        Returns:
            True if successful, False otherwise
        """
        if not AUDIO_AVAILABLE:
            print("⚠️ Audio playback not available")
            return False
            
        try:
            print(f"Playing audio: {audio_file_path}")
            
            # Load audio file
            audio_data, sample_rate = sf.read(audio_file_path)
            
            # Play audio
            sd.play(audio_data, sample_rate)
            sd.wait()  # Wait for playback to complete
            
            print("Audio playback completed")
            return True
            
        except Exception as e:
            print(f"Error playing audio: {e}")
            return False
    
    def get_available_models(self) -> list:
        """
        Get list of available Japanese TTS models
        
        Returns:
            List of available model names
        """
        if not self.tts_available:
            print("⚠️ TTS not available")
            return []
            
        try:
            # Import TTS here to avoid import errors
            from TTS.api import TTS
            
            # Get all available models
            models = TTS.list_models()
            
            # Filter Japanese models
            japanese_models = [model for model in models if '/ja/' in model]
            
            print(f"Available Japanese TTS models: {japanese_models}")
            return japanese_models
            
        except Exception as e:
            print(f"Error getting available models: {e}")
            return []
    
    def is_available(self) -> bool:
        """
        Check if TTS is available and ready
        
        Returns:
            True if TTS is ready, False otherwise
        """
        return self.tts_available and self.tts is not None