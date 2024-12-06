# setup.py

from setuptools import setup, find_packages

setup(
    name="textfromimage",
    version="0.2.0",  # Updated version
    author="Oren Grinker",
    author_email="orengr4@gmail.com",
    description="Get descriptions of images from OpenAI's GPT models on easy way.",
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url="https://github.com/OrenGrinker/textfromimage",
    packages=find_packages(),
    install_requires=[
        "openai>=1.35.15",
        "requests>=2.25.1",
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",  # Update if you choose a different license
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.9',
)
