#!/usr/bin/env python3

"""
dial package installer.
"""
import setuptools

from dial import (__author__, __description__, __license__, __requirements__,
                  __url__, __version__)
from misc import read_file

setuptools.setup(
    name="dial",
    packages=setuptools.find_packages(),
    author=__author__,
    version=__version__,
    license=__license__,
    description=__description__,
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    url=__url__,
    download_url=f"https://github.com/davafons/dial/archive/v{__version__}.tar.gz",
    entry_points={"gui_scripts": "dial = dial.__main__:main"},
    python_requires=">=3.6",
    install_requires=["".join(module_desc) for module_desc in __requirements__],
    keywords=["Deep Learning", "UI"],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: User Interfaces",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
