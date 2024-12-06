# setup.py

from setuptools import setup, find_packages

setup(
    name="ai_lab_fat",  # Name of the package
    version="4.0.1",  # Initial version
    description="A package for solving the Travelling Salesman Problem",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/ai_lab_fat",  # Replace with your repo URL
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
