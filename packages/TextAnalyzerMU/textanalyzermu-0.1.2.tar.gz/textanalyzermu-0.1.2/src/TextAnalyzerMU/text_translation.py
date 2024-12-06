from googletrans import Translator
from langdetect import detect, LangDetectException
from googletrans.exceptions import TranslationError

def text_translation(text, idioma_destino): 
    """ Translate text to a specific language with error handling.

    Args:
        text (str): Text to be translated
        idioma_destino (str): Destination language code (e.g., 'en', 'es', 'fr')

    Raises: 
        LangDetectException: If the source language cannot be detected
        TranslationError: If the translation fails due to an internal issue with the translator
        ValueError: If the language code is invalid or the destination language is not supported
        Exception: If an unexpected error occurs

    Returns:
        str: Translated text or error message
    """
    try:
        # Detect the source language
        idioma_origen = detect(text)
        
        if idioma_origen == 'und': 
            return "Error: Could not detect the source language."

        # Initialize the translator
        translator = Translator()
        
        # Perform translation
        resultado_final = translator.translate(text, src=idioma_origen, dest=idioma_destino)
        return resultado_final.text

    except LangDetectException:
        return "Error: Could not detect the language of the text."
    except TranslationError:
        return "Error: Translation failed due to an internal issue with the translator."
    except ValueError:
        return "Error: Invalid language code or destination language."
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"



