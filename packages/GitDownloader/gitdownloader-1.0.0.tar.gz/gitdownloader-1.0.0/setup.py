from setuptools import setup, find_packages

setup(
    name="GitDownloader",  # The package name
    version="1.0.0",
    author="PtPrashantTripathi",
    author_email="PtPrashantTripathi@outlook.com",
    description="A CLI tool to download GitHub folders.",
    long_description=open("README.md", mode="r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/PtPrashantTripathi/GitDownloader",
    packages=find_packages(),
    python_requires=">=3.7",
    install_requires=[
        "requests",
    ],
    entry_points={
        "console_scripts": [
            "GitDownloader=GitDownloader.cli:main",  # CLI entry point
        ],
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
