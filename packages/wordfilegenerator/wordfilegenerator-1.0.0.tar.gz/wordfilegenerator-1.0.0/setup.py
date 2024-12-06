from setuptools import setup, find_packages

setup(
    name="wordfilegenerator",
    version="1.0.0",
    description="Generate wordlist files with custom specifications.",
    author="sandrustout",
    url="https://github.com/sandrustout/unlimitedwordfilegenerator",
    packages=find_packages(),
    entry_points={
        "console_scripts": [
            "generatewordlist=main:main",
        ],
    },
)
