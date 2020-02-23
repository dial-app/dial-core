#!/usr/bin/env python3
# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Entry point for dial ui.
"""

import sys
from typing import List


def main(sys_args: List = sys.argv[1:]):
    """
    Entry point for Dial. Initialize components and stars the application.

    Args:
        sys_args: A list of arguments from the command line.
    """
    from dial.utils import initialization

    # Parse arguments
    app_config = initialization.parse_args(sys_args)

    # Initialize
    initialization.initialize_application(app_config)

    from dial.gui import app

    # Run
    sys.exit(app.run(app_config))


if __name__ == "__main__":
    main()
