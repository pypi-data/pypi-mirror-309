from setuptools import setup, find_packages
import os

# Lê o conteúdo do README.md
def read_readme():
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()

setup(
    name="AndrezaSantosCalc",
    version="1.0.2",
    author="Andreza Santos",
    description="Uma biblioteca para realizar operações básicas de uma calculadora.",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
