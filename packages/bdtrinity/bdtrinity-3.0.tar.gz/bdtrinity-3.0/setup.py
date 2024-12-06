# Copyright (C) 2024-2025 Satish Kumar S
# License: MIT

from setuptools import setup, find_packages


def readme():
    with open("README.md") as f:
        README = f.read()
    return README


with open("requirements.txt") as f:
    required = f.read().splitlines()


setup(
    name="bdtrinity",
    version="3.0",
    description="BDTrinity - An open source, low-code machine learning library in Python.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://matrix-neo.gitbook.io/bd-trinity",
    author="satish kumar",
    author_email="sathishsriram999@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    packages=find_packages(exclude=["*.tests", "*.tests.*", "tests.*", "tests"]),
    include_package_data=True,
    install_requires=required,
    #extras_require={"full": optional_required,},
)