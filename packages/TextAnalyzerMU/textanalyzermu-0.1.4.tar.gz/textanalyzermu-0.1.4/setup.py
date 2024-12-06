from setuptools import setup, find_packages

setup(
    name="TextAnalyzerMU",  # Cambia por el nombre de tu paquete
    version="0.1.4",  # Cambia según la versión del paquete
    author="Grupo G",
    author_email="naiaflorescubillas@gmail.com",
    description="Una breve descripción de tu paquete",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/izaskunbenegas/TextAnalyzer.git",  # Cambia por la URL de tu repo
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "transformers==4.46.2",  # versión compatible con TensorFlow
        "nltk>=3.9.1",  # compatible con Python 3.7 y superior
        "wordcloud==1.9.4",  # versión estable
        "matplotlib==3.9.2",  # para visualización de gráficos
        "numpy==2.0.2",  # necesario para compatibilidad con tensorflow
        "sumy==0.11.0",  # versión estable para resumen de texto
        "langdetect==1.0.9",  # compatible con la detección de idioma
        "scikit-learn==1.5.2",  # versión estable para aprendizaje automático
        "python-Levenshtein==0.26.1",  # para comparación de cadenas
        "googletrans==4.0.0rc1",  # versión compatible de Google Translate
        "pandas==2.2.3",  # necesario para manejo de datos
        "tensorflow==2.18.0"  # compatible con Keras y otras herramientas
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Cambia según tu licencia
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Cambia según la versión mínima de Python
)
