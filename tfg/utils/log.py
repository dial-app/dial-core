# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""Loggers used to show information and debug."""

import logging

logging.basicConfig(level=logging.DEBUG)

mainwindow = logging.getLogger("mainwindow")
