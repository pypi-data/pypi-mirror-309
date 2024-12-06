import nltk
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lsa import LsaSummarizer
from langdetect import detect, LangDetectException

# Download necessary resources from NLTK
nltk.download('punkt')

def summarize_text(text: str, num_sentences: int):
    """
    Extract a summary from the given text.
    
    Parameters:
    - text (str): The full text to be summarized.
    - num_sentences (int): The number of sentences in the summary.
    
    Returns:
    - str: A summary of the text with the specified number of sentences.
    
    Raises:
    - ValueError: If the text is empty or the number of sentences is invalid.
    - TypeError: If the parameters are not of the correct type.
    - LangDetectException: If language detection fails.
    """
    try:
        # Check if the text is valid and if num_sentences is a positive number
        if not isinstance(text, str):
            raise TypeError("The text must be a string.")
        if not isinstance(num_sentences, int) or num_sentences <= 0:
            raise ValueError("The number of sentences must be a positive integer.")
        if not text.strip():
            raise ValueError("The text cannot be empty.")
        
        language = detect(text)

        parser = PlaintextParser.from_string(text, Tokenizer(language))
        
        summarizer = LsaSummarizer()

        summary_sentences = summarizer(parser.document, num_sentences)

        summary = " ".join(str(sentence) for sentence in summary_sentences)
        return summary

    except LangDetectException:
        return "Error: Language detection failed."
    except ValueError as ve:
        return f"Error: {ve}"
    except TypeError as te:
        return f"Error: {te}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
