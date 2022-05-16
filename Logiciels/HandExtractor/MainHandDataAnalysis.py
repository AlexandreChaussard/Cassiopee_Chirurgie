from HandData import HandData
import tkinter as tk
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
from matplotlib import cm
import time
from Rotationnels import *
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


colorMaps = [cm.get_cmap("viridis"), cm.get_cmap("plasma"), cm.get_cmap("cool")]

def visualize_annotation(mode, annotationIndex, length=100, handPoints=[0], zEnabled=True, hand="Right", dataType="Revers", autoScale=True, threshHold=1, rotationnelActivated=True, miniRotationnel=True):
    fig = plt.figure()
    if zEnabled:
        ax = fig.gca(projection='3d')
    else:
        ax = fig.gca()
        plt.axis("off")

    point = annotationIndex
    handData.setHand(hand)
    for k in handPoints:

        if autoScale:
            x,y,z = handData.getTrajectory_autoScale_aroundAnnotation(k, annotation, point, maxDuration=length, threshold=threshHold)
        else:
            x = handData.getX_aroundAnnotation(k, annotation, point, length)
            y = handData.getY_aroundAnnotation(k, annotation, point, length)
            if zEnabled:
                z = handData.getZ_aroundAnnotation(k, annotation, point, length)
        type = handData.getMoreDataAt(mode, annotationIndex)

        x = x.reshape(1, -1)[0]
        y = y.reshape(1, -1)[0]
        if zEnabled:
            z = z.reshape(1, -1)[0]

        colorMapType = type == dataType
        for i in range(0, len(x)):
            if i + 1 >= len(x):
                break
            if zEnabled:
                ax.plot([x[i], x[i + 1]], [y[i], y[i + 1]], [z[i], z[i + 1]], color=colorMaps[colorMapType](1 - (i + 1) / len(x)))
            else:
                ax.plot([x[i], x[i + 1]], [y[i], y[i + 1]], color=colorMaps[colorMapType](1 - (i + 1) / len(x)))

            i += 2

        ax.set_xlabel('X')
        ax.set_ylabel('Y')
        if zEnabled:
            ax.set_zlabel('Z')
        if zEnabled:
            ax.plot([], [], [], label=str(type) + " " + str(k))
            if rotationnelActivated:
                rot_global = rotationnel_global([x, y, z])
                rot_color = 0.2
                rot_vect = np.array([[0, rot_global[0]],
                                    [0, rot_global[1]],
                                    [0, rot_global[2]]])
                rot_vect = rot_vect/norm(rot_global) * 0.01
                rot_vect = rot_vect + np.array([[np.mean(x)],
                                                [np.mean(y)],
                                                [np.mean(z)]])
                ax.plot(rot_vect[0],
                        rot_vect[1],
                        rot_vect[2], color=colorMaps[2](rot_color), label="Rotationnel")
                ax.plot([rot_vect[0][1]],
                        [rot_vect[1][1]],
                        [rot_vect[2][1]], color=colorMaps[2](rot_color), marker="o")
            if miniRotationnel:
                list_rot_i = rotationels_discret([x, y, z])

                j = 0
                for rot_i in list_rot_i:
                    rot_vect = np.array([[0, rot_i[0]],
                                         [0, rot_i[1]],
                                         [0, rot_i[2]]])
                    rot_vect = rot_vect / norm(rot_i) * 0.01
                    rot_vect = rot_vect + np.array([[x[j]+x[j+1]],
                                                    [y[j]+y[j+1]],
                                                    [z[j]+z[j+1]]])/2
                    ax.plot(rot_vect[0],
                            rot_vect[1],
                            rot_vect[2], color=colorMaps[2](1 - (j + 1) / len(x)), marker="_")
                    ax.plot([rot_vect[0][1]],
                            [rot_vect[1][1]],
                            [rot_vect[2][1]], color=colorMaps[2](1 - (j + 1) / len(x)), marker="o")
                    j += 1

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
    visualize_annotation(annotation,
                         annotationIndex=i,
                         length=50,
                         handPoints=[17],
                         zEnabled=True,
                         hand="Right",
                         dataType="Revers",
                         autoScale=True,
                         threshHold=0.15,
                         rotationnelActivated=True,
                         miniRotationnel=True)

plt.show()