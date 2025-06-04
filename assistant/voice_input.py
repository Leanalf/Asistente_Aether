import speech_recognition as sr
from .tts import tts

def listen_command() -> str:
    """Escucha comandos de voz con manejo de errores"""
    r = sr.Recognizer()
    try:
        with sr.Microphone() as source:
            print("\n[Escuchando...]")
            r.adjust_for_ambient_noise(source, duration=0.8)
            audio = r.listen(source, timeout=5, phrase_time_limit=6)
            
            try:
                command = r.recognize_google(audio, language="es-ES").lower()
                print(f"[Usuario]: {command}")
                return command
            except sr.UnknownValueError:
                tts.speak("No entendí lo que dijiste. ¿Puedes repetirlo?")
                return ""
            except sr.RequestError as e:
                tts.speak(f"Error en el servicio de reconocimiento: {str(e)}")
                return ""
    except sr.WaitTimeoutError:
        return ""
    except Exception as e:
        print(f"Error inesperado en listen_command: {e}")
        return ""