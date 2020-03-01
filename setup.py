#!/usr/bin/env python3

"""
dial package installer.
"""
import setuptools

from dial_core import (
    __author__,
    __description__,
    __license__,
    __requirements__,
    __url__,
    __version__,
)


def read_file(file_path):
    """
    Return the file content as a string.
    """
    return open(file_path, "r").read()


setuptools.setup(
    name="dial-core",
    packages=setuptools.find_packages(),
    author=__author__,
    version=__version__,
    license=__license__,
    description=__description__,
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    url=__url__,
    download_url=f"https://github.com/dial-app/dial-core/archive/v{__version__}.tar.gz",
    python_requires=">=3.6",
    install_requires=["".join(module_desc) for module_desc in __requirements__],
    keywords=["Deep Learning", "UI"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: User Interfaces",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
