#!python3
import tkinter as tk
from tkinter import ttk

class MyDialog:

    def __init__(self, parent, message):

        self.answer = False

        self.toplevel = tk.Toplevel(parent)
        self.labelMessage = ttk.Label(self.toplevel, text = message)
        self.labelMessage.grid(column = 2, row = 1)

        self.no_button = ttk.Button(self.toplevel, text = "Όχι", command = self.cancel)
        self.no_button.grid(column = 1, row = 2)
        self.yes_button = ttk.Button(self.toplevel, text = "Ναι", command = self.ok)
        self.yes_button.grid(column = 3, row = 2)


    def cancel(self):
        self.answer = False
        self.toplevel.destroy()   

    def ok(self):
        self.answer = True
        self.toplevel.destroy()           

    def show(self):
        self.toplevel.focus_force()
        self.toplevel.wait_window()
        return self.answer

