from setuptools import setup
from setuptools import find_packages

# Carga el contenido del README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="question-quizmaster",
    version="0.2",
    author="Mikel, Libe, Jon y Alazne",
    author_email="alazne.aramburu@alumni.mondragon.edu",
    long_description=long_description,  # Aquí va el contenido del README
    long_description_content_type="text/markdown",  # Indica que el README está en formato Markdown
    url="https://github.com/alaznearamburu/Progra_Grupal4.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
