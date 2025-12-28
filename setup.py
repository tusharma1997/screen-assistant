#!/usr/bin/env python3
"""
Setup script for Screen Context GPT Assistant
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

setup(
    name="screen-assistant",
    version="1.0.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="A Python application that allows you to ask GPT questions while automatically sharing a screenshot of your screen",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/screen-assistant",
    py_modules=["screen_assistant", "screen_assistant_gui"],
    install_requires=[
        "openai>=1.12.0",
        "pillow>=10.0.0",
        "mss>=9.0.1",
        "python-dotenv>=1.0.0",
        "rich>=13.7.0",
        "pynput>=1.7.6",
        "markdown>=3.5.1",
    ],
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Utilities",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "screen-assistant=screen_assistant:main",
            "screen-assistant-gui=screen_assistant_gui:main",
        ],
    },
)

