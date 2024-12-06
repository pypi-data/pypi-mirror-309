import os
import matplotlib.pyplot as plt
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from collections import Counter

def comun_words(texto, max_palabras=5, nombre_archivo="grafico_barras.png", tokenizar=True):
    """
    Generates a bar chart with the most frequent words in a text and saves the image in a folder.

    Args:
        texto (str): Text to analyze for the most frequent words.
        max_palabras (int): Maximum number of words to include in the chart.
        nombre_archivo (str): Name of the image file to be saved.
        tokenizar (bool): Indicates whether the text should be tokenized and filtered. If False, the entire text will be analyzed.

    Returns:
        str: Path to the generated image file with normalized paths.

    Raises:
        ValueError: If `texto` is not a string or is empty.
        Exception: For other unforeseen errors.
    """

    try:
        # Validate input text
        if not isinstance(texto, str):
            raise ValueError("Input text must be a string.")
        
        if not texto.strip():
            raise ValueError("Input text cannot be empty.")
        
        # Tokenize and filter stop words
        if tokenizar:
            palabras = word_tokenize(texto.lower())
            stop_words = set(stopwords.words('spanish'))
            palabras_filtradas = [palabra for palabra in palabras if palabra.isalpha() and palabra not in stop_words]
        else:
            palabras_filtradas = texto.split()

        if not palabras_filtradas:
            raise ValueError("No valid words found to analyze. Check the text and ensure it contains meaningful content.")

        palabra_frecuencia = Counter(palabras_filtradas)
        palabras_comunes = palabra_frecuencia.most_common(max_palabras)

        if not palabras_comunes:
            raise ValueError("No frequent words found in the text.")

        palabras, frecuencias = zip(*palabras_comunes)

        plt.figure(figsize=(12, 8))
        barras = plt.bar(palabras, frecuencias, color="#69b3a2", edgecolor="black", linewidth=1.5)

        plt.xlabel('Palabras', fontsize=14, labelpad=15, color="#333")
        plt.ylabel('Frecuencia', fontsize=14, labelpad=15, color="#333")
        plt.title('Palabras más frecuentes en el texto', fontsize=18, pad=20, color="#444")
        plt.xticks(fontsize=12, rotation=45, ha='right', color="#444")
        plt.yticks(fontsize=12, color="#444")
        plt.grid(axis='y', linestyle='--', linewidth=0.5, alpha=0.7)

        for barra in barras:
            altura = barra.get_height()
            plt.text(barra.get_x() + barra.get_width() / 2, altura + 0.5, f'{int(altura)}',
                     ha='center', va='bottom', fontsize=12, color="#444")

        carpeta = '../images_result'
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        file_path = os.path.join(carpeta, nombre_archivo).replace("\\", "/")

        plt.tight_layout()
        plt.savefig(file_path, format='png', dpi=300)

        plt.show()

        return file_path

    except ValueError as ve:
        return f"Error: {ve}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"

