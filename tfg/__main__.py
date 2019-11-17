#!/usr/bin/env python3
# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Entry point for the application.
"""

import sys

from PySide2.QtWidgets import QApplication

from tfg.mainwindow import MainWindow
from tfg.utils import log


def early_init():
    """
    Early initialization and checks needed before starting.
    """
    log.init_logs()


def main(argv):
    """
    Initialize Qt and start the program.
    """

    app = QApplication(argv)

    window = MainWindow()
    window.show()

    sys.exit(app.exec_())


if __name__ == "__main__":
    early_init()
    main(sys.argv)
