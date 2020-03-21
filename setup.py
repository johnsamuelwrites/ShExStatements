#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="shexstatements",
    version="0.0.1",
    author="John Samuel",
    author_email="johnsamuelwrites@example.com",
    description="Tool to generate shape expressions from CSV files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/johnsamuelwrites/ShExStatements",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPL v 3.0 or later",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'ply>=3.11',
    ]
    python_requires='>=3.6',
)
