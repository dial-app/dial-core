import tkinter as tk
from tkinter import messagebox


def showerror(title: str, message: str):
    root = tk.Tk()
    root.withdraw()

    messagebox.showerror(title, message)
