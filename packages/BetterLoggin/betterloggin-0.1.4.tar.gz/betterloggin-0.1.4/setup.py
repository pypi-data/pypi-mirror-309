from setuptools import setup, find_packages

setup(
    name="Betterloggin",
    version="0.1.0",
    author="Sprite Developments",
    author_email="spritedevelopments@gmail.com",
    description="An advanced logging module with colored output, JSON support, encryption, and more.",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/SpritesDevelopments/Betterloggin",
    packages=find_packages(),
    install_requires=[
        "colorama",        # For colored console output
    ],
    extras_require={
        "dev": [
            "pytest",        # For testing
            "sphinx",        # For documentation generation
            "black",         # For code formatting
            "flake8",        # For code linting
        ],
        "logging": [
            "hashlib",       # For encryption functionality
            "logging",       # Python's standard logging module (typically bundled, but explicitly mentioned for clarity)
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3 :: Only",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
    python_requires='>=3.6',
)
