# vim: ft=python fileencoding=utf-8 sts=4 sw=4 et:

"""
Utility methods to work with Tkinter.

Used for showing window messages if we can't access PySide2 (Qt), as Tkinter is
guaranteed to be installed along Python3.
"""

import tkinter as tk
from tkinter import messagebox


def showerror(message: str, title: str = "Error"):
    """
    Shows an error window with a custom message.
    """

    root = tk.Tk()
    root.withdraw()

    messagebox.showerror(title, message)
