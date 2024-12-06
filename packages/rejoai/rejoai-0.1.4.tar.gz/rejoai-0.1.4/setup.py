from setuptools import setup, find_packages
from setuptools import find_packages, setup, Extension
from Cython.Build import cythonize
import os
import shutil
import glob

setup(
    name="rejoai",                       # Package name
    version="0.1.4",                         # Initial version
    description="A brief description",       # Short description
    long_description=open("README.md").read(),  # Detailed description from README
    long_description_content_type="text/markdown",
    author="RejoAI Team",                      # Author name
    author_email="your.email@example.com",   # Author email
    url="https://github.com/rejoai",  # Project URL
    packages=find_packages(),                # Finds all modules in the package
    install_requires=[                       # Dependencies, if any
        "requests>=2.25.1",
         'cython',
    ],
    classifiers=[                            # Additional metadata
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",                 # Minimum Python version
)

