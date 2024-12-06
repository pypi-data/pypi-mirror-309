
from setuptools import setup, find_packages

setup(
    name="signavatar",
    version="0.1",
    packages=find_packages(),
    install_requires=[
        "requests",
        "imageio",
        "Pillow",
    ],
    author="Your Name",
    author_email="your.email@example.com",
    description="A library for creating sign language avatars using GIFs from Giphy.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/signavatar",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    )