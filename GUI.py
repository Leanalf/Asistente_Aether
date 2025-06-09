import customtkinter as ctk
from assistant.tts import tts
from assistant.voice_input import listen_command
from assistant.command_handler import handle_command
import threading

ctk.set_appearance_mode("dark")  # Modo oscuro
ctk.set_default_color_theme("blue")  # Tema azul

class AetherGUI(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Asistente Aether")
        self.geometry("600x400")
        self.protocol("WM_DELETE_WINDOW", self.on_closing)

        # Texto para mostrar respuestas y logs
        self.text_area = ctk.CTkTextbox(self, width=580, height=300, corner_radius=8)
        self.text_area.pack(padx=10, pady=10)

        # Frame para botones
        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=5, fill='x', padx=10)

        # Botón para activar micrófono manualmente
        self.listen_btn = ctk.CTkButton(button_frame, text="Escuchar comando", command=self.listen_command_thread)
        self.listen_btn.pack(side='left', padx=5)

        # Botón para salir
        self.exit_btn = ctk.CTkButton(button_frame, text="Salir", fg_color="red", command=self.on_closing)
        self.exit_btn.pack(side='right', padx=5)

        self.append_text("[Sistema]: Asistente Aether iniciado. Di 'ayuda' para ver comandos.\n")

    def append_text(self, text: str):
        self.text_area.insert("end", text + "\n")
        self.text_area.see("end")

    def listen_command_thread(self):
        # Ejecuta el escuchar comando en un hilo para no bloquear la GUI
        thread = threading.Thread(target=self.listen_command)
        thread.daemon = True
        thread.start()

    def listen_command(self):
        self.append_text("[Sistema]: Escuchando...")
        command = listen_command()
        if command:
            self.append_text(f"[Usuario]: {command}")
            result = handle_command(command)
            if not result:
                self.append_text("[Sistema]: No entendí el comando.")
            if "salir" in command or "terminar" in command:
                self.on_closing()

    def on_closing(self):
        tts.speak("Cerrando asistente. Hasta luego.")
        self.destroy()
