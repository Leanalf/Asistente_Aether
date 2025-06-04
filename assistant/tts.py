import pyttsx3

class TTS:
    _instance = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.engine = pyttsx3.init()
            cls._instance.engine.setProperty('rate', 160)
            cls._instance.engine.setProperty('volume', 0.9)
        return cls._instance
    
    def speak(self, text: str, wait: bool = True) -> None:
        """Sintetiza voz con manejo de errores"""
        print(f"\n[Asistente]: {text}")
        try:
            self.engine.say(text)
            if wait:
                self.engine.runAndWait()
        except Exception as e:
            print(f"Error en síntesis de voz: {e}")

tts = TTS()