#!/usr/bin/env python3

"""
dial package installer.
"""

from distutils.core import setup

import dial


setup(
    name="dial",
    packages=["dial"],
    version=dial.__version__,
    license=dial.__license__,
    description=dial.__description__,
    author=dial.__author__,
    author_email="",
    url="https://github.com/davafons/dial",
    download_url="https://github.com/davafons/dial/archive/v0.0.0a.tar.gz",
    keywords=["Deep Learning", "UI"],
    install_requires=["PySide2", "Pillow", "qimage2ndarray"],
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
