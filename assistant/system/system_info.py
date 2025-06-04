import datetime
from ..tts import tts

def get_time():
    """Obtiene la hora actual"""
    hora = datetime.datetime.now().strftime("%H:%M")
    tts.speak(f"Son las {hora}")

def get_date():
    """Obtiene la fecha actual"""
    fecha = datetime.datetime.now().strftime("%A %d de %B de %Y")
    tts.speak(f"Hoy es {fecha}")