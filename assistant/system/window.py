import pyautogui
from ..tts import tts

def maximize_window():
    """Maximiza la ventana activa"""
    try:
        win = pyautogui.getActiveWindow()
        if win:
            if not win.isMaximized:
                win.maximize()
                tts.speak("Ventana maximizada")
            else:
                tts.speak("La ventana ya está maximizada")
        else:
            tts.speak("No se pudo detectar la ventana activa")
    except Exception as e:
        tts.speak("Error al maximizar la ventana")
        print(f"Error al maximizar: {e}")

def minimize_window():
    """Minimiza la ventana activa"""
    try:
        win = pyautogui.getActiveWindow()
        if win:
            if not win.isMinimized:
                win.minimize()
                tts.speak("Ventana minimizada")
            else:
                tts.speak("La ventana ya está minimizada")
        else:
            tts.speak("No se pudo detectar la ventana activa")
    except Exception as e:
        tts.speak("Error al minimizar la ventana")
        print(f"Error al minimizar: {e}")

def restore_window():
    """Restaura la ventana a su tamaño normal"""
    try:
        win = pyautogui.getActiveWindow()
        if win:
            if win.isMaximized or win.isMinimized:
                win.restore()
                tts.speak("Ventana restaurada")
            else:
                tts.speak("La ventana ya está en tamaño normal")
        else:
            tts.speak("No se pudo detectar la ventana activa")
    except Exception as e:
        tts.speak("Error al restaurar la ventana")
        print(f"Error al restaurar: {e}")