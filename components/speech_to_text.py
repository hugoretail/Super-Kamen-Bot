# STT
# Whisper
import tempfile
import os
from typing import Optional
import numpy as np

# Try to import audio and whisper packages
try:
    import whisper
    WHISPER_AVAILABLE = True
except ImportError:
    print("⚠️ Whisper not available. Speech-to-text will be disabled.")
    print("💡 Install with: pip install openai-whisper")
    WHISPER_AVAILABLE = False
    whisper = None

try:
    import sounddevice as sd
    import soundfile as sf
    AUDIO_AVAILABLE = True
except ImportError:
    print("⚠️ Audio packages not available. Voice recording will be disabled.")
    print("💡 Install with: pip install sounddevice soundfile")
    AUDIO_AVAILABLE = False
    sd = None
    sf = None

from config import Config

class SpeechToText:
    """Speech-to-Text using OpenAI Whisper optimized for Japanese"""
    
    def __init__(self):
        """Initialize Whisper model"""
        self.model = None
        self.sample_rate = Config.SAMPLE_RATE
        self.available = False
        
        if not WHISPER_AVAILABLE:
            print("❌ Whisper not available")
            return
            
        try:
            print("Loading Whisper model...")
            # Force CPU usage to avoid GPU issues
            self.model = whisper.load_model(Config.WHISPER_MODEL, device="cpu")
            self.available = True
            print(f"Whisper model '{Config.WHISPER_MODEL}' loaded successfully on CPU")
        except Exception as e:
            print(f"❌ Failed to load Whisper model: {e}")
    
    def record_audio(self, duration: int = 5) -> Optional[np.ndarray]:
        """
        Record audio from microphone
        
        Args:
            duration: Recording duration in seconds
            
        Returns:
            Audio data as numpy array or None if error
        """
        if not AUDIO_AVAILABLE:
            print("❌ Audio recording not available")
            return None
            
        try:
            print(f"Recording for {duration} seconds...")
            audio_data = sd.rec(
                int(duration * self.sample_rate),
                samplerate=self.sample_rate,
                channels=Config.CHANNELS,
                dtype=np.float32
            )
            sd.wait()  # Wait for recording to complete
            print("Recording completed")
            return audio_data.flatten()
        except Exception as e:
            print(f"❌ Recording error: {e}")
            return None
    
    def transcribe_audio(self, audio_data: np.ndarray) -> Optional[str]:
        """
        Transcribe audio to Japanese text using Whisper
        
        Args:
            audio_data: Audio data as numpy array
            
        Returns:
            Transcribed Japanese text or None if error
        """
        if not self.available or not AUDIO_AVAILABLE:
            print("❌ Speech-to-text not available")
            return None
            
        temp_path = None
        try:
            # Ensure temp directory exists and is writable
            temp_dir = tempfile.gettempdir()
            print(f"Using temp directory: {temp_dir}")
            
            # Create temporary file for audio
            temp_fd, temp_path = tempfile.mkstemp(suffix=".wav", prefix="stt_", dir=temp_dir)
            os.close(temp_fd)  # Close file descriptor, keep the path
            
            # Save audio to temporary file
            print(f"Saving audio to temporary file: {temp_path}")
            sf.write(temp_path, audio_data, self.sample_rate)
            
            # Verify file exists and check size
            if not os.path.exists(temp_path):
                print(f"❌ Temporary file not created: {temp_path}")
                return None
            
            file_size = os.path.getsize(temp_path)
            print(f"✅ Temporary file created successfully: {temp_path} (size: {file_size} bytes)")
            
            # Test file accessibility
            try:
                with open(temp_path, 'rb') as test_file:
                    test_data = test_file.read(100)  # Read first 100 bytes
                print(f"✅ File is readable: {len(test_data)} bytes read")
            except Exception as read_error:
                print(f"❌ File read test failed: {read_error}")
                return None
            
            # Transcribe with Japanese language forced
            print("Transcribing audio to Japanese...")
            
            # Convert path to absolute path and normalize for Windows
            abs_path = os.path.abspath(temp_path)
            print(f"Using absolute path for transcription: {abs_path}")
            
            result = self.model.transcribe(
                abs_path,
                language=Config.WHISPER_LANGUAGE,
                task="transcribe",
                fp16=False  # Disable FP16 to avoid warnings
            )
            
            transcribed_text = result["text"].strip()
            print(f"Transcribed: {transcribed_text}")
            return transcribed_text
            
        except Exception as e:
            print(f"Error during transcription: {e}")
            return None
        finally:
            # Clean up temporary file
            if temp_path and os.path.exists(temp_path):
                try:
                    os.unlink(temp_path)
                    print(f"Cleaned up temporary file: {temp_path}")
                except Exception as cleanup_error:
                    print(f"Warning: Could not delete temporary file: {cleanup_error}")
    
    def transcribe_file(self, audio_file_path: str) -> Optional[str]:
        """
        Transcribe audio file to Japanese text
        
        Args:
            audio_file_path: Path to audio file
            
        Returns:
            Transcribed Japanese text or None if error
        """
        try:
            print(f"Transcribing file: {audio_file_path}")
            result = self.model.transcribe(
                audio_file_path,
                language=Config.WHISPER_LANGUAGE,
                task="transcribe"
            )
            
            transcribed_text = result["text"].strip()
            print(f"Transcribed: {transcribed_text}")
            return transcribed_text
            
        except Exception as e:
            print(f"Error during file transcription: {e}")
            return None
    
    def record_and_transcribe(self, duration: int = 5) -> Optional[str]:
        """
        Record audio and transcribe to Japanese text
        
        Args:
            duration: Recording duration in seconds
            
        Returns:
            Transcribed Japanese text or None if error
        """
        audio_data = self.record_audio(duration)
        return self.transcribe_audio(audio_data)

