from setuptools import setup, find_packages

setup(
    name="TextAnalyzerMU",  # Cambia por el nombre de tu paquete
    version="0.1.2",  # Cambia según la versión del paquete
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
        "transformers==4.30.0",
        "nltk>=3.7",
        "wordcloud==1.8.2.2",
        "matplotlib>=3.5.3",
        "numpy>=1.23.0",
        "sumy==0.8.1",
        "langdetect==1.0.9",
        "scikit-learn==1.2.2",
        "python-Levenshtein==0.20.9",
        "googletrans==4.0.0-rc1",
        "pandas>=1.4.3",
        "tensorflow>=2.10.0"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Cambia según tu licencia
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",  # Cambia según la versión mínima de Python
)
