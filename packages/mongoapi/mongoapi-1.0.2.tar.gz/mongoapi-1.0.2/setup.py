from setuptools import find_packages
from setuptools import setup

def get_long_description():
    with open("README.md", "r", encoding="utf-8") as f:
        return f.read()

setup(
    name="mongoapi",
    version="1.0.2",
    author="Paviththanan",
    author_email="rkpavi06@gmail.com",
    description="A Python package for simplifying MongoDB operations with built-in support for TTL and CRUD functionality.",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/rekcah-pavi/mongoapi",
    packages=find_packages(exclude=[]),
    python_requires=">=3.6",
    install_requires=[
        "pymongo",
    ],
    keywords="Python, MongoDB, API, Database Management, TTL, CRUD Operations, pymongo",
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Topic :: Database :: Database Engines/Servers",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
)
