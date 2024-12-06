from setuptools import setup, find_packages

setup(
    name="free_ocr",
    version="0.1.0",
    description="A simple OCR tool using Together AI.",
    long_description=open("README.md", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your_email@example.com",
    url="https://github.com/yourusername/free_ocr",
    packages=find_packages(),
    install_requires=[
        "requests>=2.0.0",
    ],
    python_requires=">=3.6",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
