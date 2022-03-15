import tkinter
import cv2
import PIL.ImageTk
import time
import matplotlib.pyplot as plt
import math
import numpy as np
from DataManager import Data
from ButtonClass import Button
from Video import VideoObject
from TopMenuClass import TopMenu
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from tkinter import Tk
from tkinter.filedialog import askopenfilename


def chooseFile():
    Tk().withdraw()
    return askopenfilename()


class App:

    def __init__(self, window, window_title, video_path):
        # Create the window
        self.window = window
        self.window.attributes('-fullscreen', True)
        self.window.bind("<space>", self.pause)
        self.window.bind("<Escape>", self.quit)
        self.window.bind("<Return>", self.addAnnotation)
        self.window.title(window_title)

        # open video source
        self.video_path = video_path
        self.vid = VideoObject(video_path)
        self.isPaused = False

        # File output
        self.annotation_file_path = video_path.replace('.avi', '_annotations.txt')
        self.file = open(self.annotation_file_path, "a+")
        self.file.close()

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(self.window, width=self.vid.width*0.85, height=self.vid.height)
        self.canvas.pack(padx=2, pady=2, side=tkinter.RIGHT)

        # File
        self.file_selector = TopMenu(window=self.window, app=self)
        self.file_selector.addEntry(label="Sélectionner une vidéo", command=chooseFile)
        # self.file_selector.pack(label="Fichier")

        # Mode menu
        self.modeList = [["Porte-aiguille", self.annot_porteAiguille, "-", ["Avec aiguille (out)", "Sans aiguille (out)", "In"]],
                         ["Pince", self.annot_pince, "-", ["Out"]],
                         ["Préférence manuelle", self.annot_manuelle, "D", ["Droitier", "Gaucher"]],
                         ["Aiguille", self.annot_aiguille, "D", ["Coup droit", "Revers", "Mixte"]],
                         ["Points", self.annot_points, "D", ["Début"]],
                         ["Fil", self.annot_fil, "D", ["Main de la pince", "Main du porte-aiguille", "Les deux mains"]],
                         ["Main dans la boîte", self.annot_mainboite, "D", ["Aucune option"]],
                         ["Noeud chirurgical", self.annot_noeud, "D", ["Serré", "Non serré", "Echec"]]]
        self.modeList = np.array(self.modeList)
        self.modeVisual = self.modeList[:, 2]
        self.mode = None
        self.mode_selector = TopMenu(window=self.window, app=self)

        for modeName, function, _, __ in self.modeList:
            self.mode_selector.addEntry(label=modeName, command=function)

        self.mode_selector.pack(label="Annotations")

        # Title
        self.annotation_button_text = tkinter.StringVar()
        self.annotation_button_text.set("Sélectionner une annotation\n dans le menu \"Annotations\"")
        self.annotation_canvas_text = tkinter.Label(self.window, textvariable=self.annotation_button_text, pady=5)
        self.annotation_canvas_text.config(font=('Helvatical bold',13))
        self.annotation_canvas_text.pack()
        # Vitesse de lecture
        self.speed = tkinter.DoubleVar()
        self.speedScale = tkinter.Scale(self.window, orient='horizontal', from_=0.1, to=4,
                                        resolution=0.1, tickinterval=2, length=550, variable=self.speed,
                                        label='Vitesse de lecture')
        self.speedScale.set(1)
        self.speedScale.pack()

        # Button to pause
        self.pause_button = Button("Pause", self.pause, self.window)
        self.pause_button.pack()
        # Button to restart
        self.reload_button = Button("Revenir au début", self.restart, self.window)
        self.reload_button.pack()
        # Button to annotate
        self.annotation_button = Button("Annoter", self.addAnnotation, self.window)
        self.annotation_button.pack()
        # Liste d'option par annotation
        self.dataOptionList = self.modeList[:, 3]
        self.dataOptionActiveList = ["Aucune option"]
        self.dataOption = tkinter.StringVar(self.window)
        self.dataOption.set(self.dataOptionActiveList[0])
        self.dataOptionMenu = tkinter.OptionMenu(self.window, self.dataOption, *self.dataOptionActiveList)
        self.dataOptionMenu.pack()

        # plot timeline et tout
        self.figureTimeLine = None
        self.cid = None
        self.axesPlot = None

        self.data = Data(self)
        self.dataIndicator = ""

        # refreshing canvas
        self.photo = None
        self.delay = 15
        self.update()

        self.plot_timeline()
        self.window.mainloop()

    def update(self):
        self.updateTimeLine()
        if self.vid.getCurrentFrameIndex() == self.vid.frame_count:
            self.window.after(self.delay, self.update)
            return
        # Get a frame from the video source
        if self.isPaused:
            ret, frame = self.vid.getCurrentView()
        else:
            ret, frame = self.vid.getNextView()
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        self.delay = int(15 * 1 / self.speed.get())
        # Relaunch update in "delay"
        self.window.after(self.delay, self.update)

    def plot_timeline(self):
        timeX = [0, self.vid.frame_count]
        timeY = [0, 0]
        timeLineX = [self.vid.getCurrentFrameIndex()]
        timeLineY = [0]
        self.figureTimeLine = plt.Figure(figsize=(6, 5), dpi=100)
        self.cid = self.figureTimeLine.canvas.mpl_connect('button_press_event', self.onClick)
        self.axesPlot = self.figureTimeLine.add_subplot()
        self.axesPlot.plot(timeX, timeY)
        self.axesPlot.plot(timeLineX, timeLineY, 'ro', markeredgewidth=1.5, markeredgecolor=(0, 0, 0, 1))
        canvas = FigureCanvasTkAgg(self.figureTimeLine, self.window)
        self.axesPlot.axis('off')
        canvas.get_tk_widget().pack(side=tkinter.LEFT)

    def updateTimeLine(self, force=False):
        if self.figureTimeLine is None:
            return
        if not force and self.vid.getCurrentFrameIndex() % 10 != 0:
            return
        plt.cla()
        plt.clf()
        self.figureTimeLine.clf()
        self.cid = self.figureTimeLine.canvas.mpl_connect('button_press_event', self.onClick)
        timeX = [0, self.vid.frame_count]
        timeY = [0, 0]
        timeLineX = [self.vid.getCurrentFrameIndex()]
        timeLineY = [0]
        self.axesPlot = self.figureTimeLine.add_subplot()
        self.axesPlot.plot(timeX, timeY)
        self.axesPlot.plot([0] + timeLineX, [0] + timeLineY, 'r')
        self.axesPlot.plot(timeLineX, timeLineY, 'ro', markeredgewidth=0.5, markeredgecolor=(0, 0, 0, 1))
        self.updateVisualData()
        self.axesPlot.axis('off')
        self.figureTimeLine.canvas.draw()
        self.figureTimeLine.canvas.flush_events()

    def updateVisualData(self):
        i = 0
        for [modeName, _, __, ___] in self.modeList:
            X, Y = self.data.getAxis(modeName)
            X.sort()
            visual = self.modeVisual[i]
            if visual != "D":
                paire = []
                abscisse = []
                for j in range(0, len(Y)):
                    paire.append(Y[j])
                    abscisse.append(X[j])
                    if len(paire) == 2:
                        self.axesPlot.plot(abscisse, paire, visual, color=self.data.colors[i])
                        paire = []
                        abscisse = []
            self.axesPlot.plot(X, Y, "D", color=self.data.colors[i], label=modeName, markersize=6, markeredgewidth=0.5, markeredgecolor=(0, 0, 0, 1))
            i += 1

        self.axesPlot.plot([0], [len(self.modeList) + 5], ".", color=[1, 1, 1])
        self.axesPlot.legend(loc='upper left', fontsize='x-small')

    def onClick(self, event):
        time, y = event.xdata, event.ydata
        buttonName = str(event.button)
        if "RIGHT" in buttonName:
            index = y if math.floor(y) == y else math.floor(y + 0.5)
            self.data.removeDataAround(time, index)
        else:
            self.vid.video.set(cv2.CAP_PROP_POS_FRAMES, time)

        self.updateTimeLine(force=True)
        self.figureTimeLine.canvas.mpl_disconnect(self.cid)

    def indexOfAnnotation(self, modeName):
        i = 0
        for mName, _, __, ___ in self.modeList:
            if mName == modeName:
                return i
            i += 1
        return i

    # -------------------------------------------------------#
    #                   Button Interactions                 #
    # -------------------------------------------------------#

    def updateTitle(self):
        self.annotation_button_text.set(self.mode)

    def updateOptions(self):
        index = self.indexOfAnnotation(self.mode)

        self.dataOptionMenu['menu'].delete(0, 'end')  # remove full list
        self.dataOptionActiveList = self.modeList[index][3]
        self.dataOption.set(self.dataOptionActiveList[0])
        for opt in self.dataOptionActiveList:
            self.dataOptionMenu['menu'].add_command(label=opt, command=tkinter._setit(self.dataOption, opt))

    def annot_porteAiguille(self):
        self.mode = "Porte-aiguille"
        self.updateOptions()
        self.updateTitle()

    def annot_fil(self):
        self.mode = "Fil"
        self.updateOptions()
        self.updateTitle()

    def annot_points(self):
        self.mode = "Points"
        self.updateOptions()
        self.updateTitle()

    def annot_aiguille(self):
        self.mode = "Aiguille"
        self.updateOptions()
        self.updateTitle()

    def annot_manuelle(self):
        self.mode = "Préférence manuelle"
        self.updateOptions()
        self.updateTitle()

    def annot_pince(self):
        self.mode = "Pince"
        self.updateOptions()
        self.updateTitle()

    def annot_noeud(self):
        self.mode = "Noeud chirurgical"
        self.updateOptions()
        self.updateTitle()

    def annot_mainboite(self):
        self.mode = "Main dans la boîte"
        self.updateOptions()
        self.updateTitle()

    def snapshot(self):
        ret, frame = self.vid.getNextView()
        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def pause(self, event=None):
        if self.vid.getCurrentFrameIndex() == self.vid.frame_count:
            return
        if self.isPaused:
            self.isPaused = False
        else:
            self.isPaused = True

    def addAnnotation(self, event=None):
        if self.mode is None:
            return
        self.data.addData(self.vid.getCurrentFrameIndex(), self.mode, self.dataOption.get())

    def restart(self):
        self.vid.video.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def stop(self):
        self.window.destroy()

    def quit(self, event=None):
        exit(0)

    def rebuild(self, title, video_path):
        if video_path == '':
            exit(0)
        self.stop()
        root = Tk()
        tkinter._default_root = root
        App(root, title, video_path)
