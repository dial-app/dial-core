# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from datetime import datetime, timedelta

"""Class used for timing the milliseconds elapsed on a block of code."""


class Timer:
    """Class used for timing the milliseconds elapsed on a block of code.

    Attributes:
        start: Moment in time when the execution started.
        end: Moment in time when the execution finished.
        running: If the block of code is still being executed.
    """

    def __enter__(self):
        """Starts tracking time."""
        self.start = datetime.now()
        self.running = True

        return self

    def __exit__(self, *args):
        """Stops tracking time."""
        self.end = datetime.now()

        self.running = False

    def interval(self) -> "timedelta":
        """Returns the interval betweent the start and end"""
        if self.running:
            return datetime.now() - self.start
        else:
            return self.end - self.start

    def elapsed(self) -> int:
        """
        Get the elapsed time (in milliseconds).
        """
        return int(self.interval().total_seconds() * 1000)
