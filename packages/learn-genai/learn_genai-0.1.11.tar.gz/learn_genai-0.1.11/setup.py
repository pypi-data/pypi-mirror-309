from setuptools import setup, find_packages

# Read the contents of README.md for the long description
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="learn_genai",
    version="0.1.11",  # Incremented version number to avoid PyPI upload conflicts
    author="Tony Esposito",
    author_email="peppedda4@gmail.com",
    description="A package to learn Generative AI through practical examples",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fbanespo1/learn_genai.git",
    packages=find_packages(),  # Automatically find packages in your project
    include_package_data=True,  # Include package data as specified in MANIFEST.in
    install_requires=[
        "streamlit",
        "langchain",
        "langchain-community",
        "langchain-ollama",
        "langgraph",
        "beautifulsoup4",
        "requests",
        "chromadb",
        "ollama",
        "transformers",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.7",
    entry_points={
    "console_scripts": [
        "learn_genai=learn_genai.run_app:main",
    ],
},
)
