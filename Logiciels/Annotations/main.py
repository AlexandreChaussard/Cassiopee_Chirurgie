from App import *

fileName = chooseFile()
tkinter.NoDefaultRoot()

if fileName == '':
    exit(0)

root = Tk()
tkinter._default_root = root
App(root, "Annotation video", video_path=fileName)