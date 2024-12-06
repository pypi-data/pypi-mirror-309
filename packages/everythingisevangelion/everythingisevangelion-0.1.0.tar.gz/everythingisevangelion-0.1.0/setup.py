from setuptools import setup, find_packages

setup(
    name="everythingisevangelion",
    version="0.1.0",
    description="Pathfinder from any Wikipedia article to Neon Genesis Evangelion",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="mwlk1",
    url="https://github.com/mwlk1/everythingisevangelion",
    packages=find_packages(),
    install_requires=[
        "requests",
        "beautifulsoup4"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
