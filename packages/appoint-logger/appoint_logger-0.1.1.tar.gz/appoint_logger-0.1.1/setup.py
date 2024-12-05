from setuptools import setup, find_packages

with open("requirements.txt") as f:
    install_requires = f.read().splitlines()

setup(
    name="appoint-logger",
    version="0.1.1",
    description="A logger package for Appoint applications",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Guy Shaked",
    author_email="dev.shakedguy@gmail.com",
    url="https://github.com/appointit-io/logger",
    packages=find_packages(),  # Automatically find package directories
    python_requires=">=3.10",
    install_requires=install_requires,
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
