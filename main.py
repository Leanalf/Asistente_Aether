from assistant.voice_input import listen_command
from assistant.command_handler import handle_command
from assistant.tts import tts

def main():
    tts.speak("Asistente iniciado. Esperando tu comando de voz.")
    while True:
        command = listen_command()
        if command == "":
            continue
        
        if "salir" in command.lower():
            tts.speak("Saliendo del asistente. ¡Hasta luego!")
            break
        
        handle_command(command)

if __name__ == "__main__":
    main()