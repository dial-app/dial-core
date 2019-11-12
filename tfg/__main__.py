#!/usr/bin/env python3
# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Entry point for the application.
"""

import sys

from PySide2.QtWidgets import QApplication

from .mainwindow import MainWindow


def main(argv):
    """
    Initialize Qt and start the program.
    """

    app = QApplication(argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    main(sys.argv)
