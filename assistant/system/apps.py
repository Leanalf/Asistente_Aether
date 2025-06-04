import os
import subprocess
import psutil
import time
from typing import Dict
from ..tts import tts

APP_PATHS = {
    "notepad": os.path.join(os.environ['WINDIR'], 'system32', 'notepad.exe'),
    "bloc de notas": os.path.join(os.environ['WINDIR'], 'system32', 'notepad.exe'),
    "calculadora": os.path.join(os.environ['WINDIR'], 'system32', 'calc.exe'),
    "explorador": "explorer.exe",
    "explorador de archivos": "explorer.exe",
    "chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "google chrome": r"C:\Program Files\Google\Chrome\Application\chrome.exe",
    "word": os.path.join(os.environ['ProgramFiles'], 'Microsoft Office', 'root', 'Office16', 'WINWORD.EXE'),
    "excel": os.path.join(os.environ['ProgramFiles'], 'Microsoft Office', 'root', 'Office16', 'EXCEL.EXE'),
    "paint": os.path.join(os.environ['WINDIR'], 'system32', 'mspaint.exe'),
}

_open_apps = {}

def get_open_apps() -> Dict[str, str]:
    """Detecta las aplicaciones abiertas"""
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

def check_app_status(app_name: str) -> bool:
    """Verifica si una aplicación está abierta"""
    app_name = app_name.lower().strip()
    get_open_apps()
    is_open = app_name in _open_apps
    tts.speak(f"{'Sí' if is_open else 'No'}, {'tienes' if is_open else 'no tienes'} {app_name} abierto")
    return is_open

def open_app(app_name: str) -> bool:
    """Abre aplicaciones con verificaciones"""
    app_name = app_name.lower().strip()
    
    known_apps = {
        'navegador': 'chrome',
        'browser': 'chrome',
        'hojas de cálculo': 'excel',
        'procesador de texto': 'word'
    }
    
    app_name = known_apps.get(app_name, app_name)
    
    if app_name not in APP_PATHS:
        available = ", ".join(sorted(APP_PATHS.keys()))
        tts.speak(f"No tengo configurada la aplicación '{app_name}'. Aplicaciones disponibles: {available}")
        return False
    
    try:
        if not os.path.exists(APP_PATHS[app_name]) and not APP_PATHS[app_name].endswith('.exe'):
            tts.speak(f"No encuentro la aplicación '{app_name}' en la ubicación esperada.")
            return False
        
        if APP_PATHS[app_name] == "explorer.exe":
            subprocess.Popen(["explorer.exe"])
        else:
            subprocess.Popen([APP_PATHS[app_name]])
        
        tts.speak(f"Abriendo {app_name}", wait=False)
        time.sleep(1)
        return True
    except Exception as e:
        tts.speak(f"No pude abrir {app_name}")
        print(f"Error al abrir aplicación: {e}")
        return False