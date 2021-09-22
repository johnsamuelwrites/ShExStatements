#
# SPDX-FileCopyrightText: 2020 John Samuel <johnsamuelwrites@gmail.com>
#
# SPDX-License-Identifier: GPL-3.0-or-later
#

import setuptools
import runpy

version_meta = runpy.run_path("./shexstatements/version.py")
VERSION = version_meta["__version__"]

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="shexstatements",
    version=VERSION,
    author="John Samuel",
    author_email="johnsamuelwrites@example.com",
    description="Tool to generate shape expressions from CSV files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/johnsamuelwrites/ShExStatements",
    packages=setuptools.find_packages(),
    scripts=["shexstatements.sh"],
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License" +
        " v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        'ply>=3.11',
        'Flask>=1.1.2',
        'PyShEx>=0.7.14',
        'sphinx-rtd-theme>=0.4.3',
        'openpyxl>=1.0.1',
        'xlrd>=2.0.1',
        'chardet>=3.0.4',
        'odfpy>=0.6.0',
    ],
    python_requires='>=3.6',
)
