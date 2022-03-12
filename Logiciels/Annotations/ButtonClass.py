import tkinter
import cv2


class Button:

    def __init__(self, buttonName, command, window):
        self.button = tkinter.Button(window, text=buttonName, width=50, command=command)

    def pack(self):
        self.button.pack(expand=True, padx=15)
