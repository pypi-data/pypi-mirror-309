import os
import re
from collections import Counter
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.data import LookupError

def mark_key_terms(texto, num_palabras=5, language='spanish', formato="html", nombre_archivo="resultado.html"):
    """
    Detects key terms in the text and highlights them in bold within an HTML file.

    Parameters:
    - texto (str): The text in which key terms will be detected and highlighted.
    - num_palabras (int): Number of key terms to highlight.
    - language (str): Language of the text (default 'spanish').
    - formato (str): Format for bolding ("html").
    - nombre_archivo (str): Name of the output HTML file.

    Returns:
    - str: Path to the generated HTML file, using standard slashes (`/`).

    Raises:
    - TypeError: If the input text is not a string.
    - ValueError: If the specified format is not valid or the number of key terms is not a positive integer.
    - LookupError: If stopwords for the specified language are not available.
    - Exception: For any unforeseen errors.
    """
    try:
        # Check if the input text is a string
        if not isinstance(texto, str):
            raise TypeError("The input text must be a string.")

        # Validate the number of words
        if not isinstance(num_palabras, int) or num_palabras <= 0:
            raise ValueError("The number of words to highlight must be a positive integer.")
        
        # Validate the format
        if formato != "html":
            raise ValueError("Invalid format. Only 'html' format is supported.")
        
        # Ensure stopwords for the specified language are available
        try:
            stopwords_list = stopwords.words(language)
        except LookupError:
            raise LookupError(f"Stopwords for language '{language}' are not available. Please download them using NLTK.")
        
        palabras = word_tokenize(texto.lower(), language=language)
        palabras_filtradas = [palabra for palabra in palabras if palabra.isalpha() and palabra not in stopwords_list]

        palabras_clave = [palabra for palabra, _ in Counter(palabras_filtradas).most_common(num_palabras)]

        palabras_negrita = {palabra: f"<b>{palabra}</b>" for palabra in palabras_clave}

        oraciones = sent_tokenize(texto, language=language)

        palabras_resaltadas = set()

        for i, oracion in enumerate(oraciones):
            for palabra, palabra_negrita in palabras_negrita.items():
                if palabra in palabras_resaltadas:
                    continue
                if palabra in oracion.lower():
                    oraciones[i] = oraciones[i].replace(palabra, palabra_negrita, 1)
                    palabras_resaltadas.add(palabra)
                    break

        texto_modificado = ' '.join(oraciones)

        carpeta = '../html_results'
        if not os.path.exists(carpeta):
            os.makedirs(carpeta)

        # Define the file path
        file_path = os.path.join(carpeta, nombre_archivo)

        file_path = file_path.replace("\\", "/")

        html_resultado = f"""
        <html>
        <head>
            <title>Texto con Palabras Clave en Negritas</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f4f4f4;
                    margin: 0;
                    padding: 0;
                    display: flex;
                    justify-content: center;
                    align-items: center;
                    height: 100vh;
                    text-align: center;
                }}
                .container {{
                    background-color: #fff;
                    border-radius: 8px;
                    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
                    padding: 20px;
                    width: 80%;
                    max-width: 800px;
                    margin-top: 20px;
                    text-align: left;
                }}
                h1 {{
                    font-size: 2rem;
                    color: #333;
                    margin-bottom: 20px;
                }}
                p {{
                    font-size: 1rem;
                    line-height: 1.6;
                    color: #333;
                }}
            </style>
        </head>
        <body>
            <div class="container">
                <h1>Texto con Palabras Clave en Negritas</h1>
                <p>{texto_modificado}</p>
            </div>
        </body>
        </html>
        """

        with open(file_path, "w", encoding="utf-8") as f:
            f.write(html_resultado)

        return file_path
    
    except TypeError as te:
        return f"Error: {te}"
    except ValueError as ve:
        return f"Error: {ve}"
    except LookupError as le:
        return f"Error: {le}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"



