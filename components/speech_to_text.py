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
    from faster_whisper import WhisperModel
    FASTER_WHISPER_AVAILABLE = True
except ImportError:
    print("⚠️ Faster-whisper not available.")
    print("💡 Install with: pip install faster-whisper")
    FASTER_WHISPER_AVAILABLE = False
    WhisperModel = None

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
        self.use_faster_whisper = False
        
        if not WHISPER_AVAILABLE and not FASTER_WHISPER_AVAILABLE:
            print("❌ No Whisper models available")
            return
            
        # Try faster-whisper first for better Windows compatibility
        if FASTER_WHISPER_AVAILABLE:
            try:
                print("Loading Faster-Whisper model...")
                self.model = WhisperModel(Config.WHISPER_MODEL, device="cpu", compute_type="int8")
                self.available = True
                self.use_faster_whisper = True
                print(f"Faster-Whisper model '{Config.WHISPER_MODEL}' loaded successfully on CPU")
                return
            except Exception as e:
                print(f"❌ Failed to load Faster-Whisper model: {e}")
        
        # Fallback to regular whisper
        if WHISPER_AVAILABLE:
            try:
                print("Loading Whisper model...")
                # Force CPU usage to avoid GPU issues
                self.model = whisper.load_model(Config.WHISPER_MODEL, device="cpu")
                self.available = True
                self.use_faster_whisper = False
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
            
        try:
            # Transcribe directly from numpy array to avoid file I/O issues
            print("Transcribing audio to Japanese...")
            
            # Ensure audio is float32 and normalized
            if audio_data.dtype != np.float32:
                audio_data = audio_data.astype(np.float32)
            
            # Normalize audio to [-1, 1] range
            if np.max(np.abs(audio_data)) > 1.0:
                audio_data = audio_data / np.max(np.abs(audio_data))
            
            # Convert stereo to mono if needed
            if audio_data.ndim > 1:
                audio_data = np.mean(audio_data, axis=1)
            
            # Resample to 16kHz if needed (Whisper expects 16kHz)
            target_sr = 16000
            if self.sample_rate != target_sr:
                # Simple resampling - for production use librosa.resample
                ratio = target_sr / self.sample_rate
                audio_data = np.interp(
                    np.linspace(0, len(audio_data), int(len(audio_data) * ratio)),
                    np.arange(len(audio_data)),
                    audio_data
                )
            
            print(f"Audio shape: {audio_data.shape}, dtype: {audio_data.dtype}")
            
            if self.use_faster_whisper:
                # Use faster-whisper with numpy array
                segments, info = self.model.transcribe(
                    audio_data,
                    language=Config.WHISPER_LANGUAGE,
                    task="transcribe"
                )
                transcribed_text = " ".join([segment.text for segment in segments]).strip()
            else:
                # Use regular whisper with numpy array
                result = self.model.transcribe(
                    audio_data,
                    language=Config.WHISPER_LANGUAGE,
                    task="transcribe",
                    fp16=False  # Disable FP16 to avoid warnings
                )
                transcribed_text = result["text"].strip()
            
            print(f"Transcribed: {transcribed_text}")
            return transcribed_text
            
        except Exception as e:
            print(f"Error during transcription: {e}")
            import traceback
            traceback.print_exc()
            return None
    
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

