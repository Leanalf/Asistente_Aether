import os
import subprocess
import psutil
import time
from typing import Dict
from ..tts import tts

# Ampliar rutas y alias de aplicaciones, incluyendo reconocimiento de voz y apps comunes
APP_PATHS = {
    "notepad": os.path.join(os.environ['WINDIR'], 'system32', 'notepad.exe'),
    "bloc de notas": os.path.join(os.environ['WINDIR'], 'system32', 'notepad.exe'),
    "calculadora": os.path.join(os.environ['WINDIR'], 'system32', 'calc.exe'),
    "explorador": "explorer.exe",
    "explorador de archivos": "explorer.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "chrome x86": r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe",
    "google chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "word": os.path.join(os.environ['ProgramFiles'], 'Microsoft Office', 'root', 'Office16', 'WINWORD.EXE'),
    "excel": os.path.join(os.environ['ProgramFiles'], 'Microsoft Office', 'root', 'Office16', 'EXCEL.EXE'),
    "paint": os.path.join(os.environ['WINDIR'], 'system32', 'mspaint.exe'),
    "cmd": os.path.join(os.environ['WINDIR'], 'system32', 'cmd.exe'),
    "powershell": os.path.join(os.environ['WINDIR'], 'system32', 'WindowsPowerShell', 'v1.0', 'powershell.exe'),
    "reconocimiento de voz": os.path.join(os.environ['WINDIR'], 'Speech', 'Common', 'sapisvr.exe'),
    "speech recognition": os.path.join(os.environ['WINDIR'], 'Speech', 'Common', 'sapisvr.exe'),
    "outlook": r"C:\Program Files\Microsoft Office\root\Office16\OUTLOOK.EXE",
    "edge": r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    "firefox": r"C:\Program Files\Mozilla Firefox\firefox.exe",
    "brave": r"C:\Program Files\BraveSoftware\Brave-Browser\Application\brave.exe",
}

_open_apps = {}

def get_open_apps() -> Dict[str, str]:
    """Detecta las aplicaciones abiertas de la lista configurada"""
    global _open_apps
    _open_apps = {}
    
    for proc in psutil.process_iter(['name', 'exe']):
        try:
            process_name = proc.info['name'].lower()
            process_exe = proc.info['exe']
            
            for app_name, app_path in APP_PATHS.items():
                if (process_name == os.path.basename(app_path).lower() or 
                    (process_exe and os.path.exists(process_exe) and 
                    os.path.samefile(process_exe, app_path))):
                    _open_apps[app_name] = "running"
        except (psutil.NoSuchProcess, psutil.AccessDenied, FileNotFoundError):
            continue
            
    if _open_apps:
        apps_list = ", ".join(_open_apps.keys())
        tts.speak(f"Tienes abiertas: {apps_list}")
    else:
        tts.speak("No detecté aplicaciones abiertas de mi lista")
    
    return _open_apps

def get_all_open_apps() -> Dict[str, str]:
    """Detecta todas las aplicaciones abiertas en tiempo real, sin depender de la lista"""
    open_apps = {}
    for proc in psutil.process_iter(['name']):
        try:
            process_name = proc.info['name']
            if process_name:
                open_apps[process_name.lower()] = "running"
        except (psutil.NoSuchProcess, psutil.AccessDenied, FileNotFoundError):
            continue

    if open_apps:
        apps_list = ", ".join(sorted(set(open_apps.keys())))
        tts.speak(f"Aplicaciones abiertas: {apps_list}")
    else:
        tts.speak("No detecté aplicaciones abiertas")
    return open_apps

def check_app_status(app_name: str) -> bool:
    """Verifica si una aplicación está abierta"""
    app_name = app_name.lower().strip()
    get_open_apps()
    is_open = app_name in _open_apps
    tts.speak(f"{'Sí' if is_open else 'No'}, {'tienes' if is_open else 'no tienes'} {app_name} abierto")
    return is_open

def open_app(app_name: str) -> bool:
    """Abre aplicaciones con verificaciones y alias mejorados"""
    app_name = app_name.lower().strip()
    
    known_apps = {
        'navegador': 'chrome',
        'browser': 'chrome',
        'hojas de cálculo': 'excel',
        'procesador de texto': 'word',
        'explorer': 'explorador',
        'explorer de archivos': 'explorador de archivos',
        'speech': 'reconocimiento de voz',
        'voz': 'reconocimiento de voz',
        'terminal': 'cmd',
        'símbolo del sistema': 'cmd',
        'powershell': 'powershell',
        'paintbrush': 'paint',
        'correo': 'outlook',
        'edge': 'edge',
        'firefox': 'firefox',
        'brave': 'brave',
    }
    
    app_name = known_apps.get(app_name, app_name)
    
    if app_name not in APP_PATHS:
        available = ", ".join(sorted(APP_PATHS.keys()))
        tts.speak(f"No tengo configurada la aplicación '{app_name}'. Aplicaciones disponibles: {available}")
        return False

    app_path = APP_PATHS[app_name]
    # Si la ruta no existe, intenta buscar en otras ubicaciones comunes para Chrome
    if app_name in ["chrome", "google chrome"] and not os.path.exists(app_path):
        alt_path = APP_PATHS.get("chrome x86")
        if alt_path and os.path.exists(alt_path):
            app_path = alt_path

    try:
        # Si es ruta absoluta y existe, abre normalmente
        if os.path.isabs(app_path) and os.path.exists(app_path):
            subprocess.Popen([app_path])
        # Si es solo el nombre del ejecutable, intenta abrirlo por nombre (debe estar en el PATH)
        elif not os.path.isabs(app_path):
            subprocess.Popen([app_path])
        else:
            tts.speak(f"No encuentro la aplicación '{app_name}' en la ubicación esperada: {app_path}")
            return False
        
        tts.speak(f"Abriendo {app_name}", wait=False)
        time.sleep(1)
        return True
    except Exception as e:
        tts.speak(f"No pude abrir {app_name}")
        print(f"Error al abrir aplicación: {e}")
        return False

def open_anything(path_or_name: str) -> bool:
    """Abre cualquier archivo, carpeta o aplicación por nombre o ruta"""
    try:
        # Si es ruta absoluta o relativa, intenta abrir con startfile
        if os.path.exists(path_or_name):
            os.startfile(path_or_name)
            tts.speak(f"Abriendo {path_or_name}")
            return True
        else:
            # Si no es ruta, intenta abrir como comando (ejecutable en PATH)
            subprocess.Popen([path_or_name])
            tts.speak(f"Ejecutando {path_or_name}")
            return True
    except Exception as e:
        tts.speak(f"No pude abrir o ejecutar {path_or_name}")
        print(f"Error al abrir o ejecutar: {e}")
        return False

# Ejemplo de control básico de pantalla
import pyautogui

def escribir_en_pantalla(texto: str):
    """Escribe texto donde esté el cursor"""
    try:
        pyautogui.write(texto)
        tts.speak("Texto escrito en pantalla")
    except Exception as e:
        tts.speak("No pude escribir en pantalla")
        print(f"Error al escribir: {e}")