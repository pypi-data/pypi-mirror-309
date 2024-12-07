from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="astro_constants",
    version="1.3.0",
    description="A Python library for common astronomical and physical constants",
    long_description=long_description,
    long_description_content_type="text/markdown",  # Explicitly specify Markdown format
    author="JoeStem",
    author_email="JoeStem25@gmail.com",
    url="https://github.com/RedGloveProductions/Astronomy",  # Replace with your repo URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
)
