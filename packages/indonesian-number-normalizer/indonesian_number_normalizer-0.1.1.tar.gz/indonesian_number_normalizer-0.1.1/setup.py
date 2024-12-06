from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="indonesian-number-normalizer",
    version="0.1.0",
    author="Ilma Aliya Fiddien",
    author_email="ilmaaliyaf@gmail.com",
    description="A package to convert numbers to Indonesian words",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/fiddien/indonesian-number-normalizer",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Natural Language :: Indonesian",
        "Topic :: Text Processing :: General",
    ],
    python_requires=">=3.7",
    install_requires=[],
    keywords=["indonesian", "number", "converter", "text normalization", "tts"],
)
