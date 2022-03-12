import tkinter
import cv2
import PIL.ImageTk
import time
import matplotlib.pyplot as plt
from ButtonClass import Button
from Video import VideoObject
from TopMenuClass import TopMenu
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class App:

    def __init__(self, window, window_title, video_path):
        # Create the window
        self.window = window
        self.window.title(window_title)

        # open video source
        self.video_path = video_path
        self.vid = VideoObject(video_path)
        self.isPaused = False
        # Refers to the index of the image beeing played
        self.currentIndex = 0

        # File output
        self.file = open(video_path.replace('avi', '_annotations.txt'), 'a+')

        # Create a canvas that can fit the above video source size
        self.canvas = tkinter.Canvas(window, width=self.vid.width * 0.8, height=self.vid.height * 0.8)
        self.canvas.pack(padx=2, side=tkinter.LEFT)

        # Mode menu
        self.mode = None
        self.mode_selector = TopMenu(window=window, app=self)

        # Qualifie In/Out avec ou sans aiguille
        self.mode_selector.addEntry(label="Porte-aiguille", command=self.annot_porteAiguille)
        # Qualifie In/Out de la pince
        self.mode_selector.addEntry(label="Pince", command=self.annot_pince)
        # Préférence manuelle
        self.mode_selector.addEntry(label="Préférence manuelle", command=self.annot_manuelle)
        # Aiguille coup droit/revers/mixte
        self.mode_selector.addEntry(label="Points/Aiguille", command=self.annot_points)
        # Main qui tend le fil (pince, porte-aguille, les deux?)
        self.mode_selector.addEntry(label="Fil", command=self.annot_fil)
        # Préférence manuelle (droitier/gaucher)
        self.mode_selector.pack(label="Annotations")

        #Title
        self.annotation_button_text = tkinter.StringVar()
        self.annotation_button_text.set("Sélectionner une annotation\n dans le menu \"Annotations\"")
        self.annotation_canvas_text = tkinter.Label(window, textvariable=self.annotation_button_text)
        self.annotation_canvas_text.pack()
        # Vitesse de lecture
        self.speed = tkinter.DoubleVar()
        self.speedScale = tkinter.Scale(window, orient='horizontal', from_=0.1, to=4,
              resolution=0.1, tickinterval=2, length=350, variable=self.speed,
              label='Vitesse de lecture')
        self.speedScale.set(1)
        self.speedScale.pack()

        # Button to pause
        self.pause_button = Button("Pause", self.pause, window)
        self.pause_button.pack()
        # Button to annotate
        self.annotation_button = Button("Annoter", self.addAnnotation, window)
        self.annotation_button.pack()
        # Button to annotate
        self.reload_button = Button("Revenir au début", self.restart, window)
        self.reload_button.pack()

        # refreshing canvas
        self.delay = 15
        self.update()

        self.plot_timeline()
        self.window.mainloop()

    def update(self):
        # Get a frame from the video source
        if self.isPaused:
            ret, frame = self.vid.getCurrentView()
        else:
            ret, frame = self.vid.getNextView()
            self.currentIndex += 1
        if ret:
            self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        self.canvas.create_image(0, 0, image=self.photo, anchor=tkinter.NW)
        self.window.after(self.delay, self.update)

    def plot_timeline(self):
        timeX = [0, self.vid.frame_count]
        timeY = [0, 0]
        figure = plt.Figure(figsize=(5, 1), dpi=100)
        axes = figure.add_subplot()
        axes.plot(timeX, timeY)
        canvas = FigureCanvasTkAgg(figure, self.window)
        axes.axis('off')
        canvas.get_tk_widget().pack(side=tkinter.LEFT)

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
        if self.isPaused:
            self.isPaused = False
        else:
            self.isPaused = True

    def addAnnotation(self):
        self.file.write(self.mode + ";" + str(self.currentIndex) + "\n")

    def restart(self):
        self.vid.video.set(2, 0)
        self.currentIndex = 0


app = App(tkinter.Tk(), "Annotation video", video_path="LEJAY_Passage1.avi")
