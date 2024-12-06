# setup.py
from setuptools import setup, find_packages
import setuptools
import os


with open("README.md", "r", encoding="utf-8") as fh:
    long_descriptions = fh.read()

setup(
    name="prismio",  # Name as seen on PyPI
    version="0.0.6",  # Increment this version for updates
    description="For now just for testing",
    long_description=long_descriptions,
    long_description_content_type="text/markdown", 
    author="Parsa",
    author_email="mehr2.business@example.com",  # Optional
    packages=find_packages(),  # Automatically find the RunwayLib packag
    entry_points={
        'console_scripts': [
            'prismio = prismio:main',
        ],
    },
    install_requires=["flask", "colorama", "zenora", "customtkinter", "tqdm", "alive_progress", "moviepy", "rabity", "keyboard"],  # List any dependencies here
    classifiers=[  # Optional, to specify the package's audience
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',  # Specify minimum Python version
)
