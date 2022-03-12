from tkinter import Menu
import tkinter

class TopMenu:

    def __init__(self, window, app):
        self.window = window
        self.app = app
        self.menubar = Menu(window)
        self.topcascade = Menu(self.menubar, tearoff=0);

    def pack(self, label):
        self.menubar.add_cascade(label=label, menu=self.topcascade)
        self.window.config(menu=self.menubar)

    def addEntry(self, label, command, separatorOnly=False):
        if separatorOnly:
            self.topcascade.add_separator()
            return
        self.topcascade.add_command(label=label, command=command)