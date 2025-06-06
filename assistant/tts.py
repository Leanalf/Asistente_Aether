import pyttsx3
from gtts import gTTS
import pygame
import tempfile
import os

class TTS:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.engine = cls._init_engine()
        return cls._instance
    
    @staticmethod
    def _init_engine():
        try:
            engine = pyttsx3.init()
            engine.setProperty('rate', 160)
            engine.setProperty('volume', 0.9)
            return engine
        except Exception:
            return None
    
    def speak(self, text: str, wait: bool = True) -> None:
        print(f"\n[Asistente]: {text}")
        
        # Intenta con pyttsx3 primero
        if self.engine:
            try:
                self.engine.say(text)
                if wait:
                    self.engine.runAndWait()
                return
            except Exception:
                pass
        
        # Fallback a gTTS
        try:
            with tempfile.NamedTemporaryFile(suffix='.mp3', delete=False) as fp:
                tts = gTTS(text=text, lang='es')
                tts.save(fp.name)
                pygame.mixer.init()
                pygame.mixer.music.load(fp.name)
                pygame.mixer.music.play()
                while pygame.mixer.music.get_busy():
                    pygame.time.Clock().tick(10)
                os.unlink(fp.name)
        except Exception as e:
            print(f"[Error TTS]: {str(e)}")

tts = TTS()