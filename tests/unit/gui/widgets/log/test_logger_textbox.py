# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import pytest

from dial.gui.widgets.log import LoggerTextboxFactory


@pytest.fixture
def logger_textbox():
    return LoggerTextboxFactory()


def test_set_plain_text(qtbot, logger_textbox):
    logger_textbox.set_plain_text("foo")

    assert logger_textbox.text == "foo"

    logger_textbox.set_plain_text("bar")

    assert logger_textbox.text == "bar"
