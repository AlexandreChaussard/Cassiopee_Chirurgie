from tkinter import Menu
import tkinter
from tkinter import Tk
from tkinter.filedialog import askopenfilename

class TopMenu:

    def __init__(self, window, app):
        self.window = window
        self.app = app
        self.menubar = Menu(window)
        self.filemenubar = Menu(window)
        self.topcascade = Menu(self.filemenubar, tearoff=0);
        self.filecascade = Menu(self.menubar, tearoff=0);

    def pack(self, label):
        self.menubar.add_cascade(label="Fichier", menu=self.filecascade)
        self.filecascade.add_command(label="Ouvrir une vidéo", command=self.openFile)
        self.menubar.add_cascade(label=label, menu=self.topcascade)
        self.window.config(menu=self.menubar)

    def addEntry(self, label, command, separatorOnly=False):
        if separatorOnly:
            self.topcascade.add_separator()
            return
        self.topcascade.add_command(label=label, command=command)

    def openFile(self):
        tkinter._default_root.withdraw()
        root = Tk()
        tkinter._default_root = root
        root.withdraw()
        fileName = askopenfilename(master=root)
        self.app.rebuild("Annotation video", video_path=fileName)