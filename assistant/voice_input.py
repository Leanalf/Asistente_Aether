import speech_recognition as sr
from .tts import tts
import time

def listen_command(timeout: int = 5, retries: int = 3) -> str:
    r = sr.Recognizer()
    
    mic_list = sr.Microphone.list_microphone_names()
    if not mic_list:
        tts.speak("No se detectó micrófono. Conecta uno e intenta nuevamente.")
        print("[Error]: No se detectó micrófono.")
        return ""
    else:
        print(f"[Micrófonos disponibles]: {mic_list}")

    # Selecciona el primer micrófono disponible
    mic_index = 0

    for attempt in range(retries):
        try:
            with sr.Microphone(device_index=mic_index) as source:
                print("\n[Escuchando...] (Di algo)")
                tts.speak("Te escucho.")
                r.adjust_for_ambient_noise(source, duration=1)
                audio = r.listen(source, timeout=timeout, phrase_time_limit=8)
                
                try:
                    text = r.recognize_google(audio, language="es-ES").lower()
                    print(f"[Usuario]: {text}")
                    return text
                except sr.UnknownValueError:
                    print("[Aviso]: No se entendió el audio.")
                    if attempt < retries - 1:
                        tts.speak("No te escuché bien, por favor repite.")
                        time.sleep(1)
                    continue
                except sr.RequestError as e:
                    tts.speak(f"Error de conexión: {str(e)}")
                    print(f"[Error de conexión]: {str(e)}")
                    return ""
                    
        except sr.WaitTimeoutError:
            print("[Aviso]: Tiempo de espera agotado.")
            tts.speak("No detecté ninguna voz. Intenta de nuevo.")
            return ""
        except Exception as e:
            print(f"[Error Micrófono]: {str(e)}")
            if attempt == retries - 1:
                tts.speak("Error en el micrófono. Revisa la conexión.")
    
    tts.speak("No se pudo reconocer el comando después de varios intentos.")
    return ""