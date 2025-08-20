# STT
# Whisper
import whisper
import sounddevice as sd
import soundfile as sf
import numpy as np
import tempfile
import os
from typing import Optional
from config import Config

class SpeechToText:
    """Speech-to-Text using OpenAI Whisper optimized for Japanese"""
    
    def __init__(self):
        """Initialize Whisper model"""
        print("Loading Whisper model...")
        self.model = whisper.load_model(Config.WHISPER_MODEL)
        self.sample_rate = Config.SAMPLE_RATE
        print(f"Whisper model '{Config.WHISPER_MODEL}' loaded successfully")
    
    def record_audio(self, duration: int = 5) -> np.ndarray:
        """
        Record audio from microphone
        
        Args:
            duration: Recording duration in seconds
            
        Returns:
            Audio data as numpy array
        """
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
    
    def transcribe_audio(self, audio_data: np.ndarray) -> Optional[str]:
        """
        Transcribe audio to Japanese text using Whisper
        
        Args:
            audio_data: Audio data as numpy array
            
        Returns:
            Transcribed Japanese text or None if error
        """
        try:
            # Create temporary file for audio
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_file:
                temp_path = temp_file.name
                
            # Save audio to temporary file
            sf.write(temp_path, audio_data, self.sample_rate)
            
            # Transcribe with Japanese language forced
            print("Transcribing audio to Japanese...")
            result = self.model.transcribe(
                temp_path,
                language=Config.WHISPER_LANGUAGE,
                task="transcribe"
            )
            
            # Clean up temporary file
            os.unlink(temp_path)
            
            transcribed_text = result["text"].strip()
            print(f"Transcribed: {transcribed_text}")
            return transcribed_text
            
        except Exception as e:
            print(f"Error during transcription: {e}")
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

