from setuptools import setup, find_packages

setup(
    name="tglexer",
    version="0.3.1",
    description="A Pygments lexer for TensorGrad language",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",  # Ensures README renders as Markdown on PyPI
    author="Vijai Kumar Suriyababu",
    author_email="vijai@tensorgrad.com",
    url="https://github.com/tensorGrad/tglexer",  # Replace with your actual GitHub repo URL
    license="MIT",
    packages=find_packages(),  # Includes tglexer as a package
    entry_points={
        "pygments.lexers": [
            "tensorgrad = tensorgrad_lexer.tensorgrad_lexer:TensorGradLexer",
        ],
    },
    python_requires=">=3.10",  # Ensures compatibility with Python 3.6+
    install_requires=[
        "pygments>=2.17",  # Pygments is required for lexer registration
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Text Processing :: Linguistic",
    ],
)
