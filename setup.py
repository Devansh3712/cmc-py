#!/usr/bin/env python

"""Module for packaging cmc-py for PyPI."""

import os
from setuptools import setup, find_packages

current_directory = os.path.dirname(os.path.realpath(__file__))

with open(
    os.path.join(current_directory, "requirements.txt"), encoding="utf-8"
) as file:
    requirements = file.readlines()

with open(os.path.join(current_directory, "README.md"), encoding="utf-8") as file:
    long_description = file.read()

if __name__ == "__main__":
    setup(
        name="cmc-py-wrapper",
        version="0.1.0",
        author="Devansh Singh",
        author_email="devanshamity@gmail.com",
        url="https://devansh3712.github.io/cmc-py/",
        download_url="https://pypi.org/project/cmc-py-wrapper/",
        project_urls={
            "Source": "https://github.com/Devansh3712/cmc-py",
            "Documentation": "https://devansh3712.github.io/cmc-py/",
        },
        description="Unofficial CoinMarketCap API and Python wrapper",
        long_description=long_description,
        long_description_content_type="text/markdown",
        license="MIT",
        packages=find_packages(
            exclude=(
                "tests",
                "api",
                "docs",
            )
        ),
        include_package_data=True,
        install_requires=requirements,
        classifiers=[
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "License :: OSI Approved :: MIT License",
            "Operating System :: Microsoft :: Windows",
        ],
    )
