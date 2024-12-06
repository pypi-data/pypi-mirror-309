import nltk
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
import string
from collections import Counter
import os

def generate_word_cloud(texto, max_palabras=100):
    """Generates a word cloud from a text

    Args:
        texto (str): Text to generate the word cloud from   
        max_palabras (int, optional): Maximum number of words to display. Defaults to 100.

    Returns:
        str: Path to the saved word cloud image.
        
    Raises:
        ValueError: If `texto` is not a string or `max_palabras` is not a positive integer.
        LookupError: If NLTK resources (stopwords or tokenizers) are missing.
        Exception: For any unforeseen errors, such as file I/O problems.
    """
    try:
        # Validate input
        if not isinstance(texto, str):
            raise ValueError("Input text must be a string.")
        
        if not isinstance(max_palabras, int) or max_palabras <= 0:
            raise ValueError("The number of words to display must be a positive integer.")

        try:
            stopwords_list = stopwords.words('spanish')
            nltk.data.find('tokenizers/punkt')
        except LookupError as e:
            raise LookupError("NLTK resources not found. Please ensure 'stopwords' and 'punkt' are downloaded.") from e

        palabras = word_tokenize(texto.lower())
        palabras_filtradas = [palabra for palabra in palabras if palabra not in stopwords_list and palabra not in string.punctuation]

        palabra_frecuencia = Counter(palabras_filtradas)
        palabras_comunes = dict(palabra_frecuencia.most_common(max_palabras))

        wordcloud = WordCloud(width=800, height=400, background_color='white').generate_from_frequencies(palabras_comunes)

        carpeta = '../images_result'
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        file_path = os.path.join(carpeta, "wordcloud.png")
        file_path = file_path.replace("\\", "/")

        plt.figure(figsize=(10, 5))
        plt.imshow(wordcloud, interpolation='bilinear')
        plt.axis('off')

        plt.savefig(file_path, format='png')

        plt.show()

        return file_path

    except ValueError as ve:
        return f"Error: {ve}"
    except LookupError as le:
        return f"Error: {le}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

