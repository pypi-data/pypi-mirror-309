import nltk
from nltk.tokenize import sent_tokenize
from nltk.data import LookupError

nltk.download('punkt')

def summarize_text(text: str, language: str):
    """
    Counts the number of sentences in a text, first detecting the language.

    Parameters:
    - text (str): The text in which the sentences will be counted.
    - language (str): Language of the text, e.g., 'english', 'spanish'.

    Returns:
    - int: The total number of sentences in the text.

    Raises:
    - TypeError: If the text is not a string.
    - ValueError: If the text is empty.
    - LookupError: If the language model for sentence tokenization is not available.
    - Exception: For any other unforeseen errors.
    """
    try:
        # Check if the input is a string
        if not isinstance(text, str):
            raise TypeError("The input text must be a string.")

        # Check if the text is empty or contains only whitespace
        if not text.strip():
            raise ValueError("The text cannot be empty or just whitespace.")

        # Tokenize the text into sentences using the specified language
        oraciones = sent_tokenize(text, language=language)
        return len(oraciones)
    
    except TypeError as te:
        return f"Error: {te}"
    except ValueError as ve:
        return f"Error: {ve}"
    except LookupError as le:
        return f"Error: Language model not found for '{language}'. Please check the language code."
    except Exception as e:
        return f"An unexpected error occurred: {e}"
