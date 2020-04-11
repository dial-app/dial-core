# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:


class Observer:
    pass


class Observable:
    def __init__(self):
        self._observers = set()

    def add_observer(self, observer: "Observer"):
        self._observers.add(observer)

    def remove_observer(self, observer: "Observer"):
        self._observers.remove(observer)
