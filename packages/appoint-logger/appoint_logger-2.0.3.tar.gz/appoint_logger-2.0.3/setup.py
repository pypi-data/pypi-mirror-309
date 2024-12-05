from setuptools import setup, find_packages


setup(
    name="appoint-logger",
    version="2.0.3",
    description="A logger package for Appoint applications",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Guy Shaked",
    author_email="dev.shakedguy@gmail.com",
    url="https://github.com/appointit-io/logger",
    packages=find_packages(),  # Automatically find package directories
    python_requires=">=3.10",
    install_requires=[
        "httpx>=0.27.2",
        "colorama>=0.4.4",
    ],
    extras_require={
        "dev": [
            # Development dependencies
            "ruff>=0.7.4",
            "pytest>=8.3.3",
            "pre-commit>=4.0.1",
            "coverage>=7.6.7",
        ]
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
