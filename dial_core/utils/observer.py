# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from typing import Callable

from dial_core.utils import log

LOGGER = log.get_logger(__name__)


class Observer:
    """This class provides an interface for classes that want to observe changes in
    other classes.

    Attributes:
        process_observer_signals: Checks if this observer should process or ignore the
        received signals.
    """

    def __init__(self):
        self.process_observer_signals = True


class Observable:
    """This class provides an interface for classes that want to be observed by other
    classes."""

    def __init__(self):
        self._observers = set()

    def notify_observers(self, signal_function: Callable, *args, **kwargs):
        """Tries to find the `signal_function` defined on each observer instance, and
        calls it.

        If the observer doesn't defines the function for processing, an exception is
        logged.
        """
        for observer in self._observers:
            if not observer.process_observer_signals:
                continue

            try:
                observer_slot = getattr(observer, signal_function.__name__)
                observer_slot(*args, **kwargs)
            except AttributeError:
                LOGGER.exception(
                    "%s does't implements %s signal.", observer, signal_function
                )

    def add_observer(self, observer: "Observer"):
        """Adds a new observer to the set of observers."""
        self._observers.add(observer)

    def remove_observer(self, observer: "Observer"):
        """Removes an observer from the set."""
        self._observers.remove(observer)
