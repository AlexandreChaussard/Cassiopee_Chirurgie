from HandData import HandData
import tkinter as tk
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
from matplotlib import cm
import time
import matplotlib as mpl
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


def chooseFile():
    tk.Tk().withdraw()
    return askopenfilename()


path = chooseFile()
if path == '':
    exit(0)

handData = HandData(path)
handData.load()

# ax = fig.add_subplot(111, projection='3d')

def visualize_annotation(mode, annotationIndex, length=100, handPoints=[0], zEnabled=True, hand="Right"):
    fig = plt.figure()
    if zEnabled:
        ax = fig.gca(projection='3d')
    else:
        ax = fig.gca()
        plt.axis("off")

    colorMap = cm.get_cmap("viridis")
    point = annotationIndex
    handData.setHand(hand)
    for k in handPoints:

        x = handData.getX_aroundAnnotation(k, annotation, point, length)
        y = handData.getY_aroundAnnotation(k, annotation, point, length)
        if zEnabled:
            z = handData.getZ_aroundAnnotation(k, annotation, point, length)
        type = handData.getMoreDataAt(mode, annotationIndex)

        x = x.reshape(1, -1)[0]
        y = y.reshape(1, -1)[0]
        if zEnabled:
            z = z.reshape(1, -1)[0]

        for i in range(0, len(x)):
            if i + 1 >= len(x):
                break
            if zEnabled:
                ax.plot([x[i], x[i + 1]], [y[i], y[i + 1]], [z[i], z[i + 1]], color=colorMap(1 - (i + 1) / len(x)))
            else:
                ax.plot([x[i], x[i + 1]], [y[i], y[i + 1]], color=colorMap(1 - (i + 1) / len(x)))

            i += 2

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        if zEnabled:
            ax.set_zlabel('Z')
        if zEnabled:
            ax.plot([], [], [], label=str(type) + " " + str(k))
        else:
            ax.plot([], [], label=str(type) + " " + str(k))
        ax.legend()

        frame = int(handData.getBeginFrameOf(mode, annotationIndex))
        fps = 25
        timeStr = time.strftime('%M:%S', time.gmtime(frame/fps))
        timeStrPushed = time.strftime('%M:%S', time.gmtime((frame+100)/fps))

        plt.title("Visualisation trajectoire : " + str(mode) + " | Main : " + hand
                  + "\nBetween frame " + str(frame) + " - " + str(frame+length)
                  + "\nBetween time " + timeStr + " - " + timeStrPushed)
        plt.pause(1)


annotation = "Aiguille"
for i in range(0, handData.getMaxAnnotationIndex(annotation)):
    visualize_annotation(annotation, annotationIndex=i, length=100, handPoints=[0], zEnabled=False, hand="Right")

plt.show()
