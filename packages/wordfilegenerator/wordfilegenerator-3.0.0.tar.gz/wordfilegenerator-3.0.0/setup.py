from setuptools import setup, find_packages

# Read the long description from README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="wordfilegenerator",
    version="3.0.0",
    description="Generate custom wordlists for brute force testing.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Sandru",
    author_email="sandrusimsone13579@gmail.com",
    license="MIT",
    packages=find_packages(),  # Automatically find all packages
    install_requires=[],  # List dependencies if any
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
