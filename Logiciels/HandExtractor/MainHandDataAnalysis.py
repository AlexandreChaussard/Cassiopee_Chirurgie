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
from PolynomialRegressor import *


def chooseFile():
    tk.Tk().withdraw()
    return askopenfilename()


path = chooseFile()
if path == '':
    exit(0)

handData = HandData(path)
handData.load()

# ax = fig.add_subplot(111, projection='3d')


colorMaps = [cm.get_cmap("viridis"), cm.get_cmap("plasma"), cm.get_cmap("viridis")]

def visualize_annotation(mode,
                         annotationIndex,
                         length=100,
                         handPoints=[0],
                         zEnabled=True,
                         hand="Right",
                         dataType="Revers",
                         autoScale=True,
                         threshHold=1,
                         rotationnelActivated=True,
                         compareRotationnels=True,
                         miniRotationnel=True,
                         miniRotationnelStep=2,
                         interpolation=True,
                         box_vitesse=True,
                         nbre_coupe=100):
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
            x_interpolated, y_interpolated, z_interpolated = polynomial_regressor(x, y, z)

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
            if interpolation:
                for i in range(0, len(x_interpolated)):
                    if i + 1 >= len(x_interpolated):
                        break
                    ax.plot([x_interpolated[i], x_interpolated[i + 1]], [y_interpolated[i], y_interpolated[i + 1]], [z_interpolated[i], z_interpolated[i + 1]],
                            color=colorMaps[colorMapType](1 - (i + 1) / len(x_interpolated)),
                            linewidth=3)
                if rotationnelActivated:
                    rot_global = rotationnel_global([x_interpolated, y_interpolated, z_interpolated])
                    if rot_global is not None:
                        rot_color = 0.2
                        rot_vect = np.array([[0, rot_global[0]],
                                            [0, rot_global[1]],
                                            [0, rot_global[2]]])
                        rot_vect = rot_vect/norm(rot_global) * 0.01
                        rot_vect = rot_vect + np.array([[np.mean(x_interpolated)],
                                                        [np.mean(y_interpolated)],
                                                        [np.mean(z_interpolated)]])
                        ax.plot(rot_vect[0],
                                rot_vect[1],
                                rot_vect[2], color=colorMaps[2](rot_color), label="Rotationnel (interpolé)")
                        ax.plot([rot_vect[0][1]],
                                [rot_vect[1][1]],
                                [rot_vect[2][1]], color=colorMaps[2](rot_color), marker="o")
            ax.plot([], [], [], label=str(type) + " " + str(k))
            if compareRotationnels:
                rot_global = rotationnel_global([x, y, z])
                rot_color = 0.9
                if rot_global is not None:
                    rot_vect = np.array([[0, rot_global[0]],
                                        [0, rot_global[1]],
                                        [0, rot_global[2]]])
                    rot_vect = rot_vect/norm(rot_global) * 0.01
                    rot_vect = rot_vect + np.array([[np.mean(x)],
                                                    [np.mean(y)],
                                                    [np.mean(z)]])
                    ax.plot(rot_vect[0],
                            rot_vect[1],
                            rot_vect[2], color=colorMaps[2](rot_color), label="Rotationnel (brut)")
                    ax.plot([rot_vect[0][1]],
                            [rot_vect[1][1]],
                            [rot_vect[2][1]], color=colorMaps[2](rot_color), marker="o")
            if miniRotationnel:
                list_rot_i, listNorm = rotationels_discret([x_interpolated, y_interpolated, z_interpolated])
                j = 0
                if list_rot_i is not None:
                    for rot_i in list_rot_i:
                        if j % miniRotationnelStep != 0:
                            j+=1
                            continue
                        rot_vect = np.array([[0, rot_i[0]],
                                             [0, rot_i[1]],
                                             [0, rot_i[2]]])
                        rot_vect = (rot_vect)*100
                        rot_vect = rot_vect + np.array([[x_interpolated[j]+x_interpolated[j+1]],
                                                        [y_interpolated[j]+y_interpolated[j+1]],
                                                        [z_interpolated[j]+z_interpolated[j+1]]])/2
                        ax.plot(rot_vect[0],
                                rot_vect[1],
                                rot_vect[2], color=colorMaps[colorMapType](1 - (j + 1) / len(x_interpolated)), marker="_")
                        ax.plot([rot_vect[0][1]],
                                [rot_vect[1][1]],
                                [rot_vect[2][1]], color=colorMaps[colorMapType](1 - (j + 1) / len(x_interpolated)), marker="o")
                        j += 1

            if box_vitesse:
                box, point_min, point_max, pas, champ_vitesse = cube_vitesse_projected([x_interpolated,
                                                                              y_interpolated,
                                                                              z_interpolated], nbre_coupe=nbre_coupe)
                if box is None:
                    continue
                for i in range(len(box[0])):
                    for j in range(len(box[1])):
                        for k in range(len(box[2])):
                            p_bot = point_min + np.array([i * pas[0],
                                                          j * pas[1],
                                                          k * pas[2]])
                            p_top = point_min + np.array([i * pas[0],
                                                          j * pas[1],
                                                          k * pas[2]]) + box[i][j][k]
                            ax.plot([p_bot[0], p_top[0]],
                                    [p_bot[1], p_top[1]],
                                    [p_bot[2], p_top[2]], marker="_", color="b")
                            ax.plot([p_top[0]],
                                    [p_top[1]],
                                    [p_top[2]], marker="o", color="b")

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
                         compareRotationnels=True,
                         miniRotationnel=True,
                         miniRotationnelStep=5,
                         interpolation=True,
                         box_vitesse=True,
                         nbre_coupe=3)

plt.show()