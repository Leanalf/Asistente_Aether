import re
import webbrowser
import pyautogui
import time
from ..tts import tts
from ..system.window import maximize_window, minimize_window, restore_window

# Soporte para varios navegadores
BROWSER_KEYWORDS = ["chrome", "firefox", "edge", "brave", "opera"]

def is_browser_focused() -> bool:
    """Verifica si el navegador tiene el foco"""
    try:
        active_window = pyautogui.getActiveWindow()
        if not active_window or not hasattr(active_window, "title"):
            return False
        return any(b in active_window.title.lower() for b in BROWSER_KEYWORDS)
    except Exception as e:
        print(f"Error al verificar foco: {e}")
        tts.speak("No pude verificar el foco del navegador.")
        return False

def focus_browser() -> bool:
    """Intenta poner el foco en el navegador"""
    try:
        for window in pyautogui.getAllWindows():
            if hasattr(window, "title") and any(b in window.title.lower() for b in BROWSER_KEYWORDS):
                window.activate()
                time.sleep(0.5)
                return True
        tts.speak("No encontré una ventana de navegador abierta.")
        return False
    except Exception as e:
        print(f"Error al enfocar navegador: {e}")
        tts.speak("No pude enfocar el navegador.")
        return False

def control_browser(command: str) -> bool:
    """Control completo del navegador"""
    command = command.lower().strip()

    # Confirmar foco antes de cada acción
    if not is_browser_focused():
        if not focus_browser():
            tts.speak("No hay navegador abierto o no pude enfocarlo.")
            return False
        time.sleep(1)
        if not is_browser_focused():
            tts.speak("No pude enfocar el navegador.")
            return False

    # Acciones del navegador con patrones ampliados
    browser_actions = {
        r'nueva pestaña|abre pestaña|pestaña nueva': ('ctrl', 't'),
        r'cerrar pestaña|cierra pestaña|cierra esta pestaña': ('ctrl', 'w'),
        r'recargar página|actualizar página|refrescar página': ('ctrl', 'r'),
        r'recargar sin caché|actualizar sin caché|refrescar sin caché': ('ctrl', 'shift', 'r'),
        r'siguiente pestaña|pestaña derecha|cambia a la derecha|avanza pestaña': ('ctrl', 'tab'),
        r'pestaña anterior|pestaña izquierda|cambia a la izquierda|retrocede pestaña': ('ctrl', 'shift', 'tab'),
        r'cerrar navegador|salir del navegador|cierra navegador': ('alt', 'f4'),
        r'ir atrás|página anterior|retroceder|atrás': ('alt', 'left'),
        r'ir adelante|página siguiente|avanzar|adelante': ('alt', 'right'),
        r'inicio|página de inicio|página principal|home': ('alt', 'home'),
        r'maximizar ventana|pantalla completa|maximizar': maximize_window,
        r'minimizar ventana|minimizar|ocultar ventana': minimize_window,
        r'restaurar ventana|tamaño normal|salir de pantalla completa|restaurar': restore_window,
        r'aumentar zoom|zoom in|acercar': ('ctrl', '+'),
        r'disminuir zoom|zoom out|alejar': ('ctrl', '-'),
        r'zoom normal|zoom predeterminado|zoom 100%': ('ctrl', '0'),
        r'abrir historial|ver historial|muestra historial': ('ctrl', 'h'),
        r'abrir descargas|ver descargas|muestra descargas': ('ctrl', 'j'),
        r'buscar en página|buscar aquí|buscar en esta página|buscar texto': ('ctrl', 'f'),
    }

    # Comando para abrir sitios web
    if re.search(r'(ir a|abrir|navegar a)\s+(.+)', command, re.IGNORECASE):
        match = re.search(r'(ir a|abrir|navegar a)\s+(.+)', command, re.IGNORECASE)
        site = match.group(2).strip()

        if not site:
            tts.speak("No especificaste a qué sitio ir.")
            return False

        site_aliases = {
            'google': 'google.com',
            'youtube': 'youtube.com',
            'facebook': 'facebook.com',
            'twitter': 'twitter.com',
            'instagram': 'instagram.com',
            'whatsapp web': 'web.whatsapp.com',
            'maps': 'maps.google.com',
            'gmail': 'mail.google.com',
            'drive': 'drive.google.com',
            'github': 'github.com',
            'outlook': 'outlook.com',
            'bing': 'bing.com',
            'reddit': 'reddit.com',
        }

        site = site_aliases.get(site, site)

        if '.' not in site:
            site = f"www.{site}.com"

        try:
            webbrowser.open(f"https://{site}")
            tts.speak(f"Navegando a {site.split('.')[1]}")
            return True
        except Exception as e:
            tts.speak(f"No pude abrir el sitio {site}")
            print(f"Error al abrir sitio: {e}")
            return False

    # Comando para buscar en Google
    elif re.search(r'(buscar|busca|googlear)\s+(.+)', command, re.IGNORECASE):
        match = re.search(r'(buscar|busca|googlear)\s+(.+)', command, re.IGNORECASE)
        query = match.group(2).strip()

        if not query:
            tts.speak("No especificaste qué buscar.")
            return False

        try:
            webbrowser.open(f"https://www.google.com/search?q={query.replace(' ', '+')}")
            tts.speak(f"Buscando {query}")
            return True
        except Exception as e:
            tts.speak("No pude realizar la búsqueda.")
            print(f"Error al buscar: {e}")
            return False

    # Comando para buscar en YouTube
    elif re.search(r'(youtube|ver en youtube|buscar en youtube)\s*(.*)', command, re.IGNORECASE):
        match = re.search(r'(youtube|ver en youtube|buscar en youtube)\s*(.*)', command, re.IGNORECASE)
        query = match.group(2).strip()

        try:
            if query:
                webbrowser.open(f"https://www.youtube.com/results?search_query={query.replace(' ', '+')}")
                tts.speak(f"Buscando {query} en YouTube")
            else:
                webbrowser.open("https://www.youtube.com")
                tts.speak("Abriendo YouTube")
            return True
        except Exception as e:
            tts.speak("No pude acceder a YouTube.")
            print(f"Error en YouTube: {e}")
            return False

    # Acciones de control del navegador
    for pattern, action in browser_actions.items():
        if re.search(pattern, command, re.IGNORECASE):
            try:
                if callable(action):
                    action()
                else:
                    # Manejo especial para teclas de zoom en algunos teclados
                    if action == ('ctrl', '+'):
                        pyautogui.hotkey('ctrl', 'add')
                    elif action == ('ctrl', '-'):
                        pyautogui.hotkey('ctrl', 'subtract')
                    else:
                        pyautogui.hotkey(*action)
                    time.sleep(0.3)

                action_name = pattern.split('|')[0]
                tts.speak(f"Listo: {action_name}")
                return True
            except Exception as e:
                tts.speak(f"No pude ejecutar la acción {pattern.split('|')[0]}")
                print(f"Error en acción de navegador: {e}")
                return False

    tts.speak("Comando de navegador no reconocido. Prueba con 'nueva pestaña', 'ir a google' o 'buscar'.")
    return False