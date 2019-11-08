#!/usr/bin/env python3
# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Entry point for the application.
"""

import sys

from PySide2.QtWidgets import QApplication, QLabel

if __name__ == "__main__":
    app = QApplication(sys.argv)

    label = QLabel("<font color=Red size=40>Hello World!</font>")
    label.show()
    app.exec_()
