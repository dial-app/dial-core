#!/usr/bin/env python3
# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Entry point for the application.
"""

import sys

from tfg.gui import app

if __name__ == "__main__":
    sys.exit(app.run(sys.argv))
