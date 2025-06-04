import re
from .web.browser import control_browser
from .web.wikipedia import search_wikipedia
from .system.apps import open_app, check_app_status, get_open_apps
from .system.system_info import get_time, get_date
from .tts import tts

def show_help():
    """Muestra los comandos disponibles"""
    help_text = """
    Comandos disponibles:
    - Información: 
      * 'Hora actual' o '¿Qué hora es?'
      * 'Fecha actual' o '¿Qué día es hoy?'
    
    - Aplicaciones: 
      * 'Abrir [nombre]' (abre aplicaciones)
      * 'Qué tengo abierto' (lista aplicaciones)
      * 'Está abierto [nombre]' (verifica una app)
    
    - Navegador: 
      * 'Nueva pestaña', 'Cerrar pestaña'
      * 'Ir a [sitio]' (ej. 'ir a google')
      * 'Buscar [término]' (busca en Google)
      * 'Recargar página', 'Página anterior/siguiente'
      * 'Maximizar/Minimizar/Restaurar ventana'
    
    - Wikipedia: 'Busca en wikipedia [tema]'
    
    - Sistema: 
      * 'Ayuda' (muestra esta ayuda)
      * 'Salir' (termina la sesión)
    """
    tts.speak(help_text)

def handle_command(command: str) -> bool:
    """Procesamiento principal de comandos"""
    if not command:
        return False
        
    if re.search(r'qué hora es|dime la hora|hora actual', command):
        get_time()
        return True
        
    if re.search(r'qué día es hoy|dime la fecha|fecha actual', command):
        get_date()
        return True
        
    if re.search(r'qué tengo abierto|aplicaciones abiertas|qué estoy usando', command):
        get_open_apps()
        return True
        
    if re.search(r'está abiert[oa] el|se está usando el|estoy usando el', command):
        app_name = re.sub(r'está abiert[oa] el|se está usando el|estoy usando el|la|el', '', command).strip()
        if app_name:
            check_app_status(app_name)
        return True
        
    if re.search(r'abrir|abre|inicia|ejecuta', command):
        app_name = re.sub(r'abrir|abre|inicia|ejecuta|la|el|por favor|\s+', ' ', command).strip()
        if app_name:
            return open_app(app_name)
        return False
    
    if re.search(r'navegador|chrome|pestaña|página|sitio|web|internet', command):
        return control_browser(command)
    
    if re.search(r'wikipedia|busca en wikipedia|consulta en wikipedia', command):
        query = re.sub(r'wikipedia|busca en wikipedia|consulta en wikipedia|en wikipedia', '', command).strip()
        return search_wikipedia(query)
    
    if re.search(r'busca|buscar|qué es|quién es', command):
        query = re.sub(r'busca|buscar|qué es|quién es|\?', '', command).strip()
        return control_browser(f"buscar {query}")
    
    if re.search(r'ayuda|qué puedes hacer|comandos', command):
        show_help()
        return True
    
    tts.speak("No entendí el comando. Di 'ayuda' para ver lo que puedo hacer")
    return False