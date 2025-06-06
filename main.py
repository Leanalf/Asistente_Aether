from assistant.voice_input import listen_command
from assistant.command_handler import handle_command
from assistant.tts import tts

def main():
    tts.speak("Asistente Aether iniciado. Di 'ayuda' para ver comandos.")
    while True:
        command = listen_command()
        if not command:
            continue
        
        if "salir" in command or "terminar" in command:
            tts.speak("Hasta luego, usuario.")
            break
        
        handle_command(command)

if __name__ == "__main__":
    main()