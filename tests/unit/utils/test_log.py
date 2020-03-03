# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

from argparse import Namespace
from unittest import mock

import pytest

from dial_core.utils import log


@pytest.fixture
def namespace():
    """
    Return a Namespace (argparse) with the default parameters.
    """
    __namespace = Namespace()
    __namespace.__setattr__("debug", False)
    __namespace.__setattr__("loglevel", "info")

    return __namespace


def test_init_with_debug(namespace):
    namespace.debug = True
    log.init_logs(namespace)

    assert log.get_log_level() == log.DEBUG


@pytest.mark.parametrize(
    "expected_log_level", ["DEBUG", "INFO", "WARNING", "CRITICAL", "ERROR"]
)
def test_init_with_log_level(namespace, expected_log_level):
    namespace.loglevel = expected_log_level
    log.init_logs(namespace)

    assert log.get_log_level() == getattr(log, expected_log_level)

    assert log.get_logger("test").level == log.get_log_level()


def test_init_with_invalid_log_level(namespace):
    namespace.loglevel = "invalid"

    # Setting an invalid log level should throw an exception
    with pytest.raises(ValueError):
        log.init_logs(namespace)


def test_log_on_start():
    logger = log.get_logger("test")

    @log.log_on_start(log.INFO, message="Log Start", logger=logger)
    def fun():
        pass

    with mock.patch.object(logger, "log") as mock_log:
        fun()

        mock_log.assert_called_once_with(log.INFO, "Log Start")


def test_log_on_end():
    logger = log.get_logger("test")

    @log.log_on_end(log.INFO, message="Log end", logger=logger)
    def fun():
        pass

    with mock.patch.object(logger, "log") as mock_log:
        fun()

        mock_log.assert_called_once_with(log.INFO, "Log end")


def test_log_on_error():
    logger = log.get_logger("test")

    @log.log_on_error(
        log.ERROR, on_exceptions=(IndexError), message="Error message", logger=logger
    )
    def fun():
        raise IndexError()

    with mock.patch.object(logger, "log") as mock_log:
        with pytest.raises(IndexError):
            fun()

        mock_log.assert_called_once_with(log.ERROR, "Error message")


def test_log_on_exception():
    logger = log.get_logger("test")

    @log.log_exception(
        on_exceptions=(IndexError), message="Exception message", logger=logger,
    )
    def fun():
        raise IndexError()

    with mock.patch.object(logger, "exception") as mock_log_exception:
        with pytest.raises(IndexError):
            fun()

        mock_log_exception.assert_called_once_with("Exception message")
