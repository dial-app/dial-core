#!/usr/bin/env python3
# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Entry point for dial ui.
"""

import argparse
import sys

from dial import __description__
from dial.gui import app
from dial.node_editor.example import run_example
from dial.utils import log


def arg_parser() -> argparse.ArgumentParser:
    """
    Return an argument parser.
    """
    parser = argparse.ArgumentParser(prog="dial", description=__description__)

    parser.add_argument(
        "-d", "--debug", help="Show debug messages", action="store_true"
    )

    parser.add_argument(
        "-l",
        "--loglevel",
        dest="loglevel",
        help="Set logging level",
        default="info",
        choices=["critical", "error", "warning", "info", "debug"],
    )

    return parser


def main():
    """
    Entry point for dial ui.
    """
    args = arg_parser().parse_args(sys.argv[1:])
    log.init_logs(args)

    # sys.exit(app.run(args))
    run_example()


if __name__ == "__main__":
    main()
