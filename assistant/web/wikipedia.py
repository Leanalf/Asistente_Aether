import wikipedia
from ..tts import tts

wikipedia.set_lang("es")

def search_wikipedia(query: str) -> bool:
    """Busca en Wikipedia y lee el resumen"""
    if not query:
        tts.speak("No especificaste qué buscar en Wikipedia")
        return False
        
    try:
        summary = wikipedia.summary(query, sentences=2, auto_suggest=True)
        tts.speak(f"Según Wikipedia: {summary}")
        return True
    except wikipedia.exceptions.DisambiguationError as e:
        options = e.options[:3]
        tts.speak(f"Hay varias opciones para {query}. Por favor sé más específico. Opciones: {', '.join(options)}")
        return False
    except wikipedia.exceptions.PageError:
        tts.speak(f"No encontré información sobre '{query}' en Wikipedia")
        return False
    except Exception as e:
        tts.speak("Ocurrió un error al consultar Wikipedia")
        print(f"Error Wikipedia: {e}")
        return False