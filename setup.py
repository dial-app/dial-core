#!/usr/bin/env python3

"""
dial package installer.
"""

import setuptools

import dial


def read_file(file_path):
    """
    Return the file content as a string.
    """
    return open(file_path, "r").read()


setuptools.setup(
    name="dial",
    packages=setuptools.find_packages(),
    author=dial.__author__,
    version=dial.__version__,
    license=dial.__license__,
    description=dial.__description__,
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/davafons/dial",
    download_url=f"https://github.com/davafons/dial/archive/v{dial.__version__}.tar.gz",
    entry_points={"gui_scripts": "dial = dial.__main__:main"},
    python_requires=">=3.6",
    install_requires=["PySide2", "Pillow", "qimage2ndarray"],
    keywords=["Deep Learning", "UI"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: User Interfaces",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
    ],
)
