# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import datetime
from unittest.mock import Mock, patch

import dial_core
from dial_core.utils import Timer


@patch.object(dial_core.utils.timer, "datetime", Mock(wraps=datetime.datetime))
def test_elapsed():
    # Start time
    dial_core.utils.timer.datetime.now.return_value = datetime.datetime(
        1, 1, 1, 0, 0, 0
    )

    with Timer() as t:
        # 1 second passed
        dial_core.utils.timer.datetime.now.return_value = datetime.datetime(
            1, 1, 1, 0, 0, 1
        )

    assert t.elapsed() == 1000


@patch.object(dial_core.utils.timer, "datetime", Mock(wraps=datetime.datetime))
def test_elapsed_while_running():
    # Start time
    dial_core.utils.timer.datetime.now.return_value = datetime.datetime(
        1, 1, 1, 0, 0, 0
    )

    with Timer() as t:
        # 1 second passed
        dial_core.utils.timer.datetime.now.return_value = datetime.datetime(
            1, 1, 1, 0, 0, 1
        )

        assert t.elapsed() == 1000

        # Another 1 second passed
        dial_core.utils.timer.datetime.now.return_value = datetime.datetime(
            1, 1, 1, 0, 0, 2
        )

        assert t.elapsed() == 2000


@patch.object(dial_core.utils.timer, "datetime", Mock(wraps=datetime.datetime))
def test_elapsed_after_stopping():
    # Start time
    dial_core.utils.timer.datetime.now.return_value = datetime.datetime(
        1, 1, 1, 0, 0, 0
    )

    with Timer() as t:
        # 1 second passed
        dial_core.utils.timer.datetime.now.return_value = datetime.datetime(
            1, 1, 1, 0, 0, 1
        )

    # Another 1 second passed
    dial_core.utils.timer.datetime.now.return_value = datetime.datetime(
        1, 1, 1, 0, 0, 2
    )

    # After stopping the Timer, elapsed should return the time elapsed only inside the
    # "with" scope
    assert t.elapsed() == 1000
