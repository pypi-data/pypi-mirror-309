from setuptools import setup, find_packages

setup(
    name="TextAnalyzerMU",  
    version="0.1.9",  
    author="Grupo G: Naia Flores, Paula Arnaiz, Izaskun Benegas y Anne Morán",
    author_email="naiaflorescubillas@gmail.com",
    description="TextAnalyzerMU",
    long_description = open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/izaskunbenegas/TextAnalyzer.git",  
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    install_requires=[
        "transformers==4.46.2",  
        "nltk==3.9.1", 
        "wordcloud==1.9.4",  
        "matplotlib==3.9.2",  
        "numpy==2.0.2", 
        "sumy==0.11.0", 
        "langdetect==1.0.9",  
        "scikit-learn==1.5.2", 
        "python-Levenshtein==0.26.1",  
        "googletrans==4.0.0rc1",  
        "pandas==2.2.3", 
        "tensorflow==2.18.0",
        "tf-keras==2.18.0"  
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  
        "Operating System :: OS Independent",
    ],
    python_requires="==3.9", 
)
