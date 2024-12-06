# E:/Library/setup.py
from setuptools import setup, find_packages

import sys
print(sys.path)


setup(
    name="library_contents",
    version="0.1",
    packages=find_packages(),
    install_requires=[],
    description="A collection of independent libraries for diff functionalities",
    author="Maitreyee_M",
    
)
