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
from ACP import *
from RotateurKleinChaussard import *
import sklearn.metrics as metrics


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
                         plotVitesse=False,
                         miniRotationnel=False,
                         miniRotationnelStep=2,
                         interpolation=True,
                         box_vitesse=True,
                         nbre_coupe=100,
                         referentiel=True):
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
            x, y, z = handData.getTrajectory_autoScale_aroundAnnotation(k, annotation, point, maxDuration=length,
                                                                        threshold=threshHold)
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
            box, point_min, point_max, pas, champ_vitesse = cube_vitesse_projected([x_interpolated,
                                                                                    y_interpolated,
                                                                                    z_interpolated],
                                                                                   nbre_coupe=nbre_coupe)
            if box is None:
                continue

        colorMapType = type == dataType
        for i in range(0, len(x)):
            if i + 1 >= len(x):
                break
            if zEnabled:
                ax.plot([x[i], x[i + 1]], [y[i], y[i + 1]], [z[i], z[i + 1]],
                        color=colorMaps[colorMapType](1 - (i + 1) / len(x)))
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
                    ax.plot([x_interpolated[i], x_interpolated[i + 1]], [y_interpolated[i], y_interpolated[i + 1]],
                            [z_interpolated[i], z_interpolated[i + 1]],
                            color=colorMaps[colorMapType](1 - (i + 1) / len(x_interpolated)),
                            linewidth=3)
                ax.plot([x_interpolated[len(x_interpolated) - 1]],
                        [y_interpolated[len(y_interpolated) - 1]],
                        [z_interpolated[len(z_interpolated) - 1]],
                        color=colorMaps[colorMapType](0.001),
                        marker="o",
                        markersize=6)
                if rotationnelActivated:
                    rot_global = rotationnel_global(box, pas,
                                                    ax=ax,
                                                    point_min=point_min,
                                                    point_max=point_max,
                                                    colorMap=colorMaps[colorMapType],
                                                    enablePlot=miniRotationnel)
                    if rot_global is not None:
                        rot_color = 0.2
                        rot_vect = np.array([[0, rot_global[0]],
                                             [0, rot_global[1]],
                                             [0, rot_global[2]]])
                        rot_vect = rot_vect / norm(rot_global) * 0.01
                        rot_vect = rot_vect + np.array([[np.mean(x_interpolated)],
                                                        [np.mean(y_interpolated)],
                                                        [np.mean(z_interpolated)]])
                        ax.plot(rot_vect[0],
                                rot_vect[1],
                                rot_vect[2], color=colorMaps[2](rot_color), label="Rotationnel (interpol??)")
                        ax.plot([rot_vect[0][1]],
                                [rot_vect[1][1]],
                                [rot_vect[2][1]], color=colorMaps[2](rot_color), marker="o")
            ax.plot([], [], [], label=str(type) + " " + str(k))
            if plotVitesse:
                list_vitesse_i, listNorm = vitesse_discret([x_interpolated, y_interpolated, z_interpolated])
                j = 0
                if list_vitesse_i is not None:
                    for vitesse_i in list_vitesse_i:
                        if j % miniRotationnelStep != 0:
                            j += 1
                            continue
                        vit_vect = np.array([[0, vitesse_i[0]],
                                             [0, vitesse_i[1]],
                                             [0, vitesse_i[2]]])
                        vit_vect = vit_vect * 100
                        vit_vect = vit_vect + np.array([[x_interpolated[j] + x_interpolated[j + 1]],
                                                        [y_interpolated[j] + y_interpolated[j + 1]],
                                                        [z_interpolated[j] + z_interpolated[j + 1]]]) / 2
                        ax.plot(vit_vect[0],
                                vit_vect[1],
                                vit_vect[2], color=colorMaps[colorMapType](1 - (j + 1) / len(x_interpolated)),
                                marker="_")
                        ax.plot([vit_vect[0][1]],
                                [vit_vect[1][1]],
                                [vit_vect[2][1]], color=colorMaps[colorMapType](1 - (j + 1) / len(x_interpolated)),
                                marker="o")
                        j += 1

            if box_vitesse:
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
        if referentiel:
            plot_referentiel([x_interpolated, y_interpolated, z_interpolated], axis=ax, multiplier=0.01)
        if rotationnelActivated:
            plot_rot_global([x_interpolated, y_interpolated, z_interpolated],
                            axis=ax,
                            plotVitesse=False,
                            plotAcceleration=False,
                            plotMiniRot=True,
                            multiplier=0.05)
        ax.legend()

        frame = int(handData.getBeginFrameOf(mode, annotationIndex))
        fps = 25
        timeStr = time.strftime('%M:%S', time.gmtime(frame / fps))
        timeStrPushed = time.strftime('%M:%S', time.gmtime((frame + length) / fps))

        plt.title("Visualisation trajectoire : " + str(mode) + " | Main : " + hand
                  + "\nBetween frame " + str(frame) + " - " + str(frame + length)
                  + "\nBetween time " + timeStr + " - " + timeStrPushed)
        plt.pause(1)


annotation = "Aiguille"
if False:
    for i in range(0, handData.getMaxAnnotationIndex(annotation)):
        visualize_annotation(annotation,
                             annotationIndex=i,
                             length=80,
                             handPoints=[17],
                             zEnabled=True,
                             hand="Right",
                             dataType="Revers",
                             autoScale=True,
                             threshHold=0.15,
                             rotationnelActivated=True,
                             plotVitesse=False,
                             miniRotationnel=False,
                             miniRotationnelStep=5,
                             interpolation=True,
                             box_vitesse=False,
                             nbre_coupe=3,
                             referentiel=True)

    plt.show()


def compute_rotationel_global(annotationIndex,
                              hand="Right",
                              handPoint=17,
                              nbre_coupe=5,
                              length=100,
                              threshHold=1):
    point = annotationIndex
    handData.setHand(hand)
    x, y, z = handData.getTrajectory_autoScale_aroundAnnotation(handPoint,
                                                                annotation,
                                                                point,
                                                                maxDuration=length,
                                                                threshold=threshHold)

    x = x.reshape(1, -1)[0]
    y = y.reshape(1, -1)[0]
    z = z.reshape(1, -1)[0]
    x_interpolated, y_interpolated, z_interpolated = polynomial_regressor(x, y, z)
    box, point_min, point_max, pas, champ_vitesse = cube_vitesse_projected([x_interpolated,
                                                                            y_interpolated,
                                                                            z_interpolated],
                                                                           nbre_coupe=nbre_coupe)
    return rotationnel_global(box, pas)


def compute_normal_vector(annotationIndex,
                          hand="Right",
                          handPoint=17,
                          length=100,
                          threshHold=1):
    point = annotationIndex
    handData.setHand(hand)
    x, y, z = handData.getTrajectory_autoScale_aroundAnnotation(handPoint,
                                                                annotation,
                                                                point,
                                                                maxDuration=length,
                                                                threshold=threshHold)

    x = x.reshape(1, -1)[0]
    y = y.reshape(1, -1)[0]
    z = z.reshape(1, -1)[0]
    x_interpolated, y_interpolated, z_interpolated = polynomial_regressor(x, y, z)
    [u, v, w] = find_base([x_interpolated, y_interpolated, z_interpolated])
    return w


def compute_rotateur(annotationIndex,
                     hand="Right",
                     handPoint=17,
                     length=100,
                     threshHold=1):
    point = annotationIndex
    handData.setHand(hand)
    x, y, z = handData.getTrajectory_autoScale_aroundAnnotation(handPoint,
                                                                annotation,
                                                                point,
                                                                maxDuration=length,
                                                                threshold=threshHold)

    x = x.reshape(1, -1)[0]
    y = y.reshape(1, -1)[0]
    z = z.reshape(1, -1)[0]
    x_interpolated, y_interpolated, z_interpolated = polynomial_regressor(x, y, z)
    return rotateur_global([x_interpolated, y_interpolated, z_interpolated])


def plot_all_rotationnels(mode="Aiguille",
                          hand="Right",
                          handPoint=17,
                          nbre_coupe=5,
                          length=100,
                          threshHold=1,
                          saveFile=False):
    if saveFile:
        file = open("rotationnels.txt", 'a+')

    fig = plt.figure()
    ax = fig.gca(projection='3d')
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    for annotationIndex in range(0, handData.getMaxAnnotationIndex(mode)):
        type = handData.getMoreDataAt(mode, annotationIndex)
        rot_global = compute_rotationel_global(annotationIndex, hand, handPoint, nbre_coupe, length, threshHold)
        rotateur_interpol = compute_rotateur(annotationIndex, hand, handPoint, length, threshHold)
        w = compute_normal_vector(annotationIndex, hand, handPoint, length, threshHold)
        colorMapType = type == "Revers"
        colorMap = colorMaps[colorMapType]
        rot_color = 0.6

        if saveFile:
            line = type + ";rotationnel=[" + str(rot_global[0]) + ":" + str(rot_global[1]) + ":" + str(
                rot_global[2]) + "];" \
                   + "w=[" + str(w[0]) + ":" + str(w[1]) + ":" + str(w[2]) + "];" \
                   + "rotateur=[" + str(rotateur_interpol[0]) + ":" + str(rotateur_interpol[1]) + ":" + str(
                rotateur_interpol[2]) + "];" \
                   + handData.name + ";\n"
            if line not in open(file.name, 'r').read():
                file.write(line)

        rot_global = rotateur_interpol / norm(rotateur_interpol)
        rot_vect = np.array([[0, rot_global[0]],
                             [0, rot_global[1]],
                             [0, rot_global[2]]])
        ax.plot(rot_vect[0],
                rot_vect[1],
                rot_vect[2], color=colorMap(rot_color))
        ax.plot([rot_vect[0][1]],
                [rot_vect[1][1]],
                [rot_vect[2][1]], color=colorMap(rot_color), marker="o")

    if saveFile:
        file.close()
        print("rotationnels.txt saved.")
    plt.show()


#plot_all_rotationnels(mode="Aiguille", saveFile=True)

def unwrap_rotationels():
    file = open("rotationnels.txt", 'r')
    inviduals = []
    types = []
    rotationnels = []
    w = []
    rotateurs = []
    for line in file.readlines():
        seria = line.split(";")
        type = seria[0]
        rotSeria = seria[1].replace("rotationnel=[", "").replace("]", "").split(":")
        rot_x, rot_y, rot_z = float(rotSeria[0]), float(rotSeria[1]), float(rotSeria[2])
        wSeria = seria[2].replace("w=[", "").replace("]", "").split(":")
        w_x, w_y, w_z = float(wSeria[0]), float(wSeria[1]), float(wSeria[2])
        rotateurSeria = seria[3].replace("rotateur=[", "").replace("]", "").split(":")
        rotateur_x, rotateur_y, rotateur_z = float(rotateurSeria[0]), float(rotateurSeria[1]), float(rotateurSeria[2])
        types.append(type)
        inviduals.append(seria[len(seria)-2])
        rotationnels.append(np.array([rot_x, rot_y, rot_z]))
        rotateurs.append(np.array([rotateur_x, rotateur_y, rotateur_z]))
        w.append(np.array([w_x, w_y, w_z]))

    file.close()
    return types, inviduals, rotationnels, w, rotateurs


def plot_all_inviduals(selectedIndividuals=None):
    types, individus, rotationnels, w, rotateurs = unwrap_rotationels()

    plot_legend = []
    data = []
    for i in range(0, len(types)):
        individu = individus[i]
        if selectedIndividuals:
            skip = True
            for ind in selectedIndividuals:
                if ind in individu:
                    skip = False
                    break
            if skip:
                continue
        type = types[i]
        rotateur_global = rotateurs[i]
        rot_global = rotationnels[i]
        w_vector = w[i]
        colorMapType = type == "Revers"
        colorMap = colorMaps[colorMapType]

        prod_scal_rot = np.dot(w_vector, rot_global)
        prod_scal_rotateur = np.dot(w_vector, rotateur_global)

        data.append([prod_scal_rotateur < 0, colorMapType])
        # plt.plot([prod_scal_rot], [colorMapType], marker="o", color=colorMap(0.6))
        plt.plot([prod_scal_rotateur], [colorMapType + 0.5], marker="o", color=colorMap(0.6))

        if colorMapType not in plot_legend:
            plt.plot([], [], marker="o", color=colorMap(0.6), label=type)
            plot_legend.append(colorMapType)

    data = np.array(data)
    data = data.T
    y_true = data[1:2][0]
    y_pred = data[0:1][0]
    confusion = metrics.confusion_matrix(y_true, y_pred)
    print(str(selectedIndividuals))
    print(confusion)

    if selectedIndividuals:
        plt.title(str(selectedIndividuals))

    plt.legend()
    plt.show()


plot_all_inviduals()
plot_all_inviduals(selectedIndividuals=["CHAKFE", "AUBERTIN", "BONNIN", "BRATU"])
plot_all_inviduals(selectedIndividuals=["BRATU"])
plot_all_inviduals(selectedIndividuals=["BONNIN"])
plot_all_inviduals(selectedIndividuals=["CHAKFE"])
plot_all_inviduals(selectedIndividuals=["AUBERTIN"])