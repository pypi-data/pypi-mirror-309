from setuptools import setup, find_packages

setup(
    name="JornadaRPA.WebScrap",  
    version="0.1.0",  
    author="Alex Diogo",  
    author_email="alexdiogo@desafiosrpa.com.br",
    description="Módulo de scraping de tabelas web para o JornadaRPA",  
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",  
    url="https://github.com/JornadaRPA/JornadaRPA.WebScrap",  
    packages=find_packages(),  
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[  
        "botcity-framework-web",  
        "pandas",       
    ],
)
