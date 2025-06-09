import threading
from assistant.voice_input import listen_command
from assistant.command_handler import handle_command
from assistant.tts import tts
from GUI import AetherGUI

def voice_loop():
    tts.speak("Asistente Aether iniciado. Di 'ayuda' para ver comandos.")
    while True:
        command = listen_command()
        if not command:
            continue
        
        if "salir" in command or "terminar" in command:
            tts.speak("Hasta luego, usuario.")
            # Aquí puedes agregar un evento para cerrar la GUI también si quieres
            break
        
        handle_command(command)

def main():
    gui = AetherGUI()

    voice_thread = threading.Thread(target=voice_loop, daemon=True)
    voice_thread.start()

    gui.mainloop()

if __name__ == "__main__":
    main()
