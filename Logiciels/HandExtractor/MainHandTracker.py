from MediaPipe_Hands import HandTracker
import tkinter as tk
from tkinter.filedialog import askopenfilename


def chooseFile():
    tk.Tk().withdraw()
    return askopenfilename()


path = chooseFile()
if path == '':
    exit(0)

tracker = HandTracker(path)
tracker.launch()
