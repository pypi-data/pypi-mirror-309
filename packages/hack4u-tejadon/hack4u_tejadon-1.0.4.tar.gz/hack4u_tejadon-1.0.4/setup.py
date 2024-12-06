#!/usr/bin/env python3

from setuptools import setup, find_packages

# Leer el contenido del archivo README.md
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="hack4u_tejadon",
    version="1.0.4",
    packages=find_packages(),
    install_requires=[],
    author="Jesús T.",
    description="Una biblioteca para consultar curso de hack4u",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://hack4u.io"
)