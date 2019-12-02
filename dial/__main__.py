#!/usr/bin/env python3
# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Entry point for dial ui.
"""

import sys

from dial.gui import app


def main():
    """
    Entry point for dial ui.
    """
    sys.exit(app.run(sys.argv))


if __name__ == "__main__":
    main()
