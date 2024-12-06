from googletrans import Translator
from langdetect import detect, LangDetectException
from googletrans import LANGUAGES  # Optional, for validating language codes

def text_translation(text, idioma_destino): 
    """ Translate text to a specific language with error handling.

    Args:
        text (str): Text to be translated
        idioma_destino (str): Destination language code (e.g., 'en', 'es', 'fr')

    Raises: 
        LangDetectException: If the source language cannot be detected
        ValueError: If the translation fails or invalid language code is provided
        Exception: If an unexpected error occurs

    Returns:
        str: Translated text or error message
    """
    try:
        # Detect the source language
        idioma_origen = detect(text)
        
        if idioma_origen == 'und': 
            return "Error: Could not detect the source language."

        # Validate if destination language is supported
        if idioma_destino not in LANGUAGES:
            raise ValueError(f"Error: Language '{idioma_destino}' is not supported.")
        
        # Initialize the translator
        translator = Translator()
        
        # Perform translation
        resultado_final = translator.translate(text, src=idioma_origen, dest=idioma_destino)
        return resultado_final.text

    except LangDetectException:
        return "Error: Could not detect the language of the text."
    except ValueError as ve:
        return f"Error: {ve}"
    except Exception as e:
        return f"An unexpected error occurred: {str(e)}"

# texto2 = 'Happiness often hides in the simple things: the sound of leaves rustling in the wind, the warm embrace of someone you love, or that song that makes you dance without realizing it. It’s a state we create with the little details, a spark that lights up our hearts when we allow ourselves to savor the present moment. '
# print(text_translation(texto2, idioma_destino='es'))

