from setuptools import setup, find_packages

setup(
    name="AndrezaSantosCalc",
    version="1.0.1",
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
