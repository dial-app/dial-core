"""
Utility methods to work with Tkinter.

Used for showing window messages if we can't access PySide2 (PyQt5), as Tkinter is
guaranteed to be installed along Python3.
"""

import tkinter as tk
from tkinter import messagebox


def showerror(message: str, title: str = "Error"):
    """
    Show an error window with a custom message.
    """

    root = tk.Tk()
    root.withdraw()

    messagebox.showerror(title, message)
