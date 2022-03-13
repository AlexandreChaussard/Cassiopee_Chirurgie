import tkinter
import cv2
import PIL.ImageTk
import time
import matplotlib.pyplot as plt
import math
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
        self.canvas = tkinter.Canvas(self.window, width=self.vid.width * 0.8, height=self.vid.height * 0.8)
        self.canvas.pack(padx=2, side=tkinter.LEFT)

        # File
        self.file_selector = TopMenu(window=self.window, app=self)
        self.file_selector.addEntry(label="Sélectionner une vidéo", command=chooseFile)
        self.file_selector.pack(label="Fichier")

        # Mode menu
        self.modeList = [["Porte-aiguille", self.annot_porteAiguille],
                         ["Pince", self.annot_pince],
                         ["Préférence manuelle", self.annot_manuelle],
                         ["Points/Aiguille", self.annot_points],
                         ["Fil", self.annot_fil]]
        self.modeVisual = ["-", "-", "D", "D", "D"]
        self.mode = None
        self.mode_selector = TopMenu(window=self.window, app=self)

        for modeName, function in self.modeList:
            self.mode_selector.addEntry(label=modeName, command=function)

        self.mode_selector.pack(label="Annotations")

        # Title
        self.annotation_button_text = tkinter.StringVar()
        self.annotation_button_text.set("Sélectionner une annotation\n dans le menu \"Annotations\"")
        self.annotation_canvas_text = tkinter.Label(self.window, textvariable=self.annotation_button_text)
        self.annotation_canvas_text.pack()
        # Vitesse de lecture
        self.speed = tkinter.DoubleVar()
        self.speedScale = tkinter.Scale(self.window, orient='horizontal', from_=0.1, to=4,
                                        resolution=0.1, tickinterval=2, length=350, variable=self.speed,
                                        label='Vitesse de lecture')
        self.speedScale.set(1)
        self.speedScale.pack()

        # Button to pause
        self.pause_button = Button("Pause", self.pause, self.window)
        self.pause_button.pack()
        # Button to annotate
        self.annotation_button = Button("Annoter", self.addAnnotation, self.window)
        self.annotation_button.pack()
        # Button to annotate
        self.reload_button = Button("Revenir au début", self.restart, self.window)
        self.reload_button.pack()

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
        self.figureTimeLine = plt.Figure(figsize=(5, 3), dpi=100)
        self.cid = self.figureTimeLine.canvas.mpl_connect('button_press_event', self.onClick)
        self.axesPlot = self.figureTimeLine.add_subplot()
        self.axesPlot.plot(timeX, timeY)
        self.axesPlot.plot(timeLineX, timeLineY, 'ro')
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
        self.axesPlot.plot(timeLineX, timeLineY, 'ro')
        self.axesPlot.plot([0] + timeLineX, [0] + timeLineY, 'r')
        self.updateVisualData()
        self.axesPlot.axis('off')
        self.figureTimeLine.canvas.draw()
        self.figureTimeLine.canvas.flush_events()

    def updateVisualData(self):
        i = 0
        for [modeName, _] in self.modeList:
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
            self.axesPlot.plot(X, Y, "D", color=self.data.colors[i])
            i += 1

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

    # -------------------------------------------------------#
    #                   Button Interactions                 #
    # -------------------------------------------------------#

    def updateTitle(self):
        self.annotation_button_text.set(self.mode)

    def annot_porteAiguille(self):
        self.mode = "Porte-aiguille"
        self.updateTitle()

    def annot_fil(self):
        self.mode = "Fil"
        self.updateTitle()

    def annot_points(self):
        self.mode = "Points/Aiguille"
        self.updateTitle()

    def annot_manuelle(self):
        self.mode = "Préférence manuelle"
        self.updateTitle()

    def annot_pince(self):
        self.mode = "Pince"
        self.updateTitle()

    def snapshot(self):
        ret, frame = self.vid.getNextView()
        if ret:
            cv2.imwrite("frame-" + time.strftime("%d-%m-%Y-%H-%M-%S") + ".jpg", cv2.cvtColor(frame, cv2.COLOR_RGB2BGR))

    def pause(self):
        if self.vid.getCurrentFrameIndex() == self.vid.frame_count:
            return
        if self.isPaused:
            self.isPaused = False
        else:
            self.isPaused = True

    def addAnnotation(self):
        if self.mode is None:
            return
        self.data.addData(self.vid.getCurrentFrameIndex(), self.mode, self.dataIndicator)

    def restart(self):
        self.vid.video.set(cv2.CAP_PROP_POS_FRAMES, 0)

    def stop(self):
        self.window.destroy()

    def rebuild(self, title, video_path):
        if video_path == '':
            exit(0)
        self.stop()
        root = Tk()
        tkinter._default_root = root
        App(root, title, video_path)
