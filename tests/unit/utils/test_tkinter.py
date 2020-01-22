# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

import tkinter
from unittest.mock import patch

from dial.utils import tkinter as dial_tkinter


@patch.object(tkinter.messagebox, "showerror")
def test_showerror(mock_showerror):
    title = "title"
    message = "message"

    dial_tkinter.showerror(message, title)

    mock_showerror.assert_called_with(title, message)
