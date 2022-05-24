import numpy as np
from sklearn.mixture import GaussianMixture
from numpy import quantile, where, random


def rotationels_discret(trajectory):
    X = trajectory[0]
    Y = trajectory[1]
    Z = trajectory[2]

    list = []
    listNorm = []
    for i in range(0, len(X) - 2):
        rot_i_x = X[i + 1] - X[i]
        rot_i_y = Y[i + 1] - Y[i]
        rot_i_z = Z[i + 1] - Z[i]
        #rot_i_x = ((Z[i + 2] - 2 * Z[i + 1] + Z[i]) / (Y[i + 1] - Y[i]) - (Y[i + 2] - 2 * Y[i + 1] + Y[i]) / (
        #        Z[i + 1] - Z[i]))
        #rot_i_y = ((X[i + 2] - 2 * X[i + 1] + X[i]) / (Z[i + 1] - Z[i]) - (Z[i + 2] - 2 * Z[i + 1] + Z[i]) / (
        #        X[i + 1] - X[i]))
        #rot_i_z = ((Y[i + 2] - 2 * Y[i + 1] + Y[i]) / (X[i + 1] - X[i]) - (X[i + 2] - 2 * X[i + 1] + X[i]) / (
        #        Y[i + 1] - Y[i]))
        rot_i = [rot_i_x, rot_i_y, rot_i_z]
        listNorm.append(norm(rot_i))
        list.append(np.array(rot_i))

    if list is None or listNorm is None or len(list) < 2 or len(listNorm) < 2:
        return None, None

    #listNorm = np.array(listNorm).reshape(-1, 1)
    #gmm = GaussianMixture().fit(listNorm)
    #scores = gmm.score_samples(listNorm)
    #thresh = quantile(scores, .1)
    #index = where(scores > thresh)[0]

    #list = np.array(list)[index]
    #listNorm = np.array(listNorm)[index]

    return list, listNorm


def norm(vect):
    return (vect[0] ** 2 + vect[1] ** 2 + vect[2] ** 2) ** .5


def rotationnel_global(trajectory):
    X = trajectory[0]
    Y = trajectory[1]
    Z = trajectory[2]
    list_rot_discret, listNorm = rotationels_discret(trajectory)
    if list_rot_discret is None or len(list_rot_discret) == 0:
        return

    rot_global = None
    for i in range(0, len(list_rot_discret)):
        rot_i = list_rot_discret[i]
        vector_i = np.array([[X[i]],
                             [Y[i]],
                             [Z[i]]])
        vector_i_plus_1 = np.array([[X[i + 1]],
                                    [Y[i + 1]],
                                    [Z[i + 1]]])
        if rot_global is None:
            rot_global = rot_i * norm(vector_i_plus_1 - vector_i)
        else:
            rot_global += rot_i * norm(vector_i_plus_1 - vector_i)

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

        return v_opt * ponderator(normes[index]) * 100

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


