from setuptools import setup, find_packages

setup(
    name='AndrezaSantosCalc',
    version='1.0.3',
    packages=find_packages(),
    description='Uma biblioteca para realizar operações básicas de uma calculadora.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Andreza Santos',
    author_email='seu_email@example.com',
    license='MIT',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
)

