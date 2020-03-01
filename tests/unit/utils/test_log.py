# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

# import logging
# from argparse import Namespace

# import pytest

# from dial_core.utils import log

# @pytest.fixture
# def namespace():
#     """
#     Return a Namespace (argparse) with the default parameters.
#     """
#     __namespace = Namespace()
#     __namespace.__setattr__("debug", False)
#     __namespace.__setattr__("loglevel", "info")

#     return __namespace


# def test_init_with_debug(namespace):
#     namespace.debug = True
#     log.init_logs(namespace)

#     assert log.LOG_LEVEL == log.DEBUG


# @pytest.mark.parametrize(
#     "expected_log_level", ["DEBUG", "INFO", "WARNING", "CRITICAL", "ERROR"]
# )
# def test_init_with_log_level(namespace, expected_log_level):
#     namespace.loglevel = expected_log_level
#     log.init_logs(namespace)

#     assert log.LOG_LEVEL == getattr(log, expected_log_level)

#     assert log.get_logger("test").level == log.LOG_LEVEL


# def test_init_with_invalid_log_level(namespace):
#     namespace.loglevel = "invalid"

#     # Setting an invalid log level should throw an exception
#     with pytest.raises(ValueError):
#         log.init_logs(namespace)
