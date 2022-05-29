import numpy as np
from sklearn.mixture import GaussianMixture
from numpy import quantile, where, random


def vitesse_discret(trajectory):
    X = trajectory[0]
    Y = trajectory[1]
    Z = trajectory[2]

    list = []
    listNorm = []
    for i in range(0, len(X) - 2):
        rot_i_x = X[i + 1] - X[i]
        rot_i_y = Y[i + 1] - Y[i]
        rot_i_z = Z[i + 1] - Z[i]
        rot_i = [rot_i_x, rot_i_y, rot_i_z]
        listNorm.append(norm(rot_i))
        list.append(np.array(rot_i))

    if list is None or listNorm is None or len(list) < 2 or len(listNorm) < 2:
        return None, None

    return list, listNorm


def norm(vect):
    return (vect[0] ** 2 + vect[1] ** 2 + vect[2] ** 2) ** .5


def rotationnel_global(box, pas, ax=None, point_min=None, point_max=None, colorMap=None, enablePlot=None):

    rot_vectors = []

    (x_size, y_size, z_size) = box.shape
    for i in range(0, x_size-1):
        for j in range(0, y_size-1):
            for k in range(0, z_size-1):
                rot_x = (box[i+1][j+1][k+1][2] - box[i][j][k][2])/pas[1] \
                        + (box[i+1][j+1][k+1][1] - box[i][j][k][1])/pas[2]
                rot_y = (box[i+1][j+1][k+1][0] - box[i][j][k][0])/pas[2] \
                        + (box[i+1][j+1][k+1][2] - box[i][j][k][2])/pas[0]
                rot_z = (box[i+1][j+1][k+1][1] - box[i][j][k][1])/pas[0] \
                        + (box[i+1][j+1][k+1][0] - box[i][j][k][0])/pas[1]
                rot_vector = np.array([rot_x, rot_y, rot_z]) * norm(np.array([pas[0],
                                                                              pas[1],
                                                                              pas[2]]))
                rot_vectors.append(rot_vector)

    rot_vectors = np.array(rot_vectors)
    rot_global = np.sum(rot_vectors, axis=0)

    if enablePlot:

        def findMax(matrix):
            maxVector = None
            for i in range(0, len(matrix)):
                vector = matrix[i]
                if maxVector is None:
                    maxVector = vector
                if norm(maxVector) < norm(vector):
                    maxVector = vector
            return maxVector

        divider = norm(findMax(rot_vectors))
        index = 0
        for i in range(0, x_size-1):
            for j in range(0, y_size-1):
                for k in range(0, z_size-1):
                    rot_vector = (rot_vectors[index]/divider)
                    index += 1
                    if norm(rot_vector) < 0.1:
                        continue
                    rot_vector = rot_vector*0.05
                    rot_x, rot_y, rot_z = rot_vector[0], rot_vector[1], rot_vector[2]
                    point_quadrillage = point_min + np.array([i * pas[0],
                                                              j * pas[1],
                                                              k * pas[2]])
                    x = np.array([point_quadrillage[0], point_quadrillage[0] + rot_x])
                    y = np.array([point_quadrillage[1], point_quadrillage[1] + rot_y])
                    z = np.array([point_quadrillage[2], point_quadrillage[2] + rot_z])
                    ax.plot(x, y, z, color=colorMap(1 - (i + 1) / x_size))
                    ax.plot([x[1]], [y[1]], [z[1]], color=colorMap(1 - (i + 1) / x_size), marker="o")

    return rot_global

def cube_vitesse(trajectory, nbre_coupe):
    def ponderator(x):
        return 2 /(1 + np.exp(np.tan(np.pi/2 * (x - 0.0001))))

    def ponderated_neighbour(point_quadrillage, champ_vitesse, trajectory):
        ponderated_v = None
        X = trajectory[0]
        Y = trajectory[1]
        Z = trajectory[2]
        poids = 0
        normes = []
        for i in range(0, len(champ_vitesse)):
            x_i, y_i, z_i = X[i], Y[i], Z[i]
            point = np.array([x_i, y_i, z_i])
            norm_value = norm(point - point_quadrillage)
            normes.append(norm_value)
        normes = np.array(normes)
        mean_norm = np.min(normes)
        normes = (normes - np.min(normes))/(np.max(normes) - np.min(normes))

        for i in range(0, len(champ_vitesse)):
            v_i = champ_vitesse[i]
            norm_value = normes[i]
            p = ponderator(norm_value)
            poids += p
            if ponderated_v is None:
                ponderated_v = v_i * ponderator(norm_value)
            else:
                ponderated_v += v_i * ponderator(norm_value)
        return ponderated_v/poids*(1/(0.005 + mean_norm**2))

    champ_vitesse = []
    X = trajectory[0]
    Y = trajectory[1]
    Z = trajectory[2]

    if len(trajectory) < 3 or len(X) < 1:
        return None, None, None, None, None

    for i in range(0, len(X) - 1):
        v_x = X[i + 1] - X[i]
        v_y = Y[i + 1] - Y[i]
        v_z = Z[i + 1] - Z[i]
        v = np.array([v_x, v_y, v_z])
        champ_vitesse.append(v)
    champ_vitesse = np.array(champ_vitesse)

    x_min, y_min, z_min = np.min(X), np.min(Y), np.min(Z)
    x_max, y_max, z_max = np.max(X), np.max(Y), np.max(Z)
    pas_x = (x_max - x_min) / nbre_coupe
    pas_y = (y_max - y_min) / nbre_coupe
    pas_z = (z_max - z_min) / nbre_coupe
    pas = np.array([pas_x, pas_y, pas_z])
    point_min = np.array([x_min, y_min, z_min]) - pas
    point_max = np.array([x_max, y_max, z_max]) + pas

    box = np.zeros((nbre_coupe+3, nbre_coupe+3, nbre_coupe+3), dtype=object)
    for i in range(0, nbre_coupe + 3):
        for j in range(0, nbre_coupe + 3):
            for k in range(0, nbre_coupe + 3):
                point_quadrillage = point_min + np.array([i * pas_x,
                                                          j * pas_y,
                                                          k * pas_z])
                ponderated_v = ponderated_neighbour(point_quadrillage, champ_vitesse, trajectory)
                box[i][j][k] = np.array(ponderated_v)

    return box, point_min, point_max, pas, champ_vitesse

def cube_vitesse_projected(trajectory, nbre_coupe):
    def ponderator(x):
        return np.exp(-x**5)

    def ponderated_neighbour(point_quadrillage, champ_vitesse, trajectory):
        X = trajectory[0]
        Y = trajectory[1]
        Z = trajectory[2]
        normes = []
        for i in range(0, len(champ_vitesse)):
            x_i, y_i, z_i = X[i], Y[i], Z[i]
            point = np.array([x_i, y_i, z_i])
            norm_value = norm(point - point_quadrillage)
            normes.append(norm_value)
        normes = np.array(normes)
        normes = (normes - np.min(normes))/(np.max(normes) - np.min(normes))
        index = np.argmin(normes)
        v_opt = champ_vitesse[index]

        return v_opt * ponderator(normes[index])

    champ_vitesse = []
    X = trajectory[0]
    Y = trajectory[1]
    Z = trajectory[2]

    if len(trajectory) < 3 or len(X) < 1:
        return None, None, None, None, None

    for i in range(0, len(X) - 1):
        v_x = X[i + 1] - X[i]
        v_y = Y[i + 1] - Y[i]
        v_z = Z[i + 1] - Z[i]
        v = np.array([v_x, v_y, v_z])
        champ_vitesse.append(v)
    champ_vitesse = np.array(champ_vitesse)

    x_min, y_min, z_min = np.min(X), np.min(Y), np.min(Z)
    x_max, y_max, z_max = np.max(X), np.max(Y), np.max(Z)
    pas_x = (x_max - x_min) / nbre_coupe
    pas_y = (y_max - y_min) / nbre_coupe
    pas_z = (z_max - z_min) / nbre_coupe
    pas = np.array([pas_x, pas_y, pas_z])
    point_min = np.array([x_min, y_min, z_min]) - pas
    point_max = np.array([x_max, y_max, z_max]) + pas

    box = np.zeros((nbre_coupe+3, nbre_coupe+3, nbre_coupe+3), dtype=object)
    for i in range(0, nbre_coupe + 3):
        for j in range(0, nbre_coupe + 3):
            for k in range(0, nbre_coupe + 3):
                point_quadrillage = point_min + np.array([i * pas_x,
                                                          j * pas_y,
                                                          k * pas_z])
                ponderated_v = ponderated_neighbour(point_quadrillage, champ_vitesse, trajectory)
                box[i][j][k] = np.array(ponderated_v)

    return box, point_min, point_max, pas, champ_vitesse


