#!/usr/bin/env python3
"""
Setup script for enahaplots library.
This file ensures proper package building and installation.
"""

from setuptools import setup, find_packages

setup(
    name="enahaplots",
    version="1.0.0",
    description="A personal Python visualization library with themed charts and statistical analysis",
    author="Enaha",
    author_email="enaha@example.com",
    license="MIT",
    packages=find_packages(include=["enahaplots", "enahaplots.*"]),
    python_requires=">=3.8",
    install_requires=[
        "matplotlib>=3.5.0",
        "numpy>=1.20.0",
        "scipy>=1.7.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Scientific/Engineering :: Visualization",
    ],
)
