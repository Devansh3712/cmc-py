#!/usr/bin/env python

"""Module for packaging cmc-py for PyPI."""

import os
from setuptools import setup, find_packages

current_directory = os.path.dirname(os.path.realpath(__file__))

with open(os.path.join(current_directory, "README.md"), encoding="utf-8") as file:
    long_description = file.read()

if __name__ == "__main__":
    setup(
        name="cmc-py-wrapper",
        version="0.1.3",
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
        install_requires=[
            "async-generator==1.10",
            "attrs==21.4.0",
            "beautifulsoup4==4.10.0",
            "certifi==2021.10.8",
            "cffi==1.15.0",
            "charset-normalizer==2.0.12",
            "colorama==0.4.4",
            "configparser==5.2.0",
            "crayons==0.4.0",
            "cryptography==36.0.1",
            "h11==0.13.0",
            "idna==3.3",
            "lxml==4.8.0",
            "outcome==1.1.0",
            "pycparser==2.21",
            "pyOpenSSL==22.0.0",
            "requests==2.27.1",
            "selenium==4.1.0",
            "sniffio==1.2.0",
            "sortedcontainers==2.4.0",
            "soupsieve==2.3.1",
            "trio==0.19.0",
            "trio-websocket==0.9.2",
            "urllib3==1.26.8",
            "webdriver-manager==3.5.3",
            "wsproto==1.0.0",
        ],
        classifiers=[
            "Programming Language :: Python :: 3.9",
            "Programming Language :: Python :: 3.10",
            "License :: OSI Approved :: MIT License",
            "Operating System :: Microsoft :: Windows",
        ],
    )
