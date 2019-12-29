# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from datetime import datetime


class Timer:
    def __enter__(self):
        self.start = datetime.now()
        self.running = True

        return self

    def __exit__(self, *args):
        self.end = datetime.now()

        self.running = False

    def interval(self):
        if self.running:
            return datetime.now() - self.start
        else:
            return self.end - self.start

    def elapsed(self):
        """
        Get elapsed time (in milliseconds).
        """
        return int(self.interval().total_seconds() * 1000)
