# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""Loggers used to display information and debug."""

import logging

mainwindow = logging.getLogger("mainwindow")


def init_logs():
    """
    Initialize logging system.
    """

    logging.basicConfig(level=logging.DEBUG)
