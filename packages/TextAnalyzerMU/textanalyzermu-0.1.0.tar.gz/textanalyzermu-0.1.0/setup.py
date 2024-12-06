from setuptools import setup, find_packages

setup(
    name="TextAnalyzerMU",  # Cambia por el nombre de tu paquete
    version="0.1.0",  # Cambia según la versión del paquete
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
        "transformers",
        "nltk",
        "wordcloud",
        "matplotlib",
        "sumy",
        "langdetect",
        "scikit-learn",
        "python-Levenshtein",
        "googletrans==4.0.0-rc1",
        "pandas",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Cambia según tu licencia
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Cambia según la versión mínima de Python
)
