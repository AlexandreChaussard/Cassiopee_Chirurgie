import numpy as np
from sklearn.mixture import GaussianMixture
from numpy import quantile, where, random

def rotationels_discret(trajectory):
    X = trajectory[0]
    Y = trajectory[1]
    Z = trajectory[2]

    list = []
    listNorm = []
    for i in range(0, len(X)-2):
        rot_i_x = ((Z[i+2]-2*Z[i+1]+Z[i])/(Y[i+1]-Y[i]) - (Y[i+2]-2*Y[i+1]+Y[i])/(Z[i+1]-Z[i]))
        rot_i_y = ((X[i+2]-2*X[i+1]+X[i])/(Z[i+1]-Z[i]) - (Z[i+2]-2*Z[i+1]+Z[i])/(X[i+1]-X[i]))
        rot_i_z = ((Y[i+2]-2*Y[i+1]+Y[i])/(X[i+1]-X[i]) - (X[i+2]-2*X[i+1]+X[i])/(Y[i+1]-Y[i]))
        rot_i = [rot_i_x, rot_i_y, rot_i_z]
        listNorm.append(norm(rot_i))
        list.append(np.array(rot_i))

    if list is None or listNorm is None or len(list) < 2 or len(listNorm) < 2:
        return None, None

    listNorm = np.array(listNorm).reshape(-1, 1)
    gmm = GaussianMixture().fit(listNorm)
    scores = gmm.score_samples(listNorm)
    thresh = quantile(scores, .1)
    index = where(scores > thresh)[0]

    list = np.array(list)[index]
    listNorm = np.array(listNorm)[index]

    return list, listNorm

def norm(vect):
    return (vect[0]**2 + vect[1]**2 + vect[2]**2)**.5

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
        vector_i_plus_1 = np.array([[X[i+1]],
                                    [Y[i+1]],
                                    [Z[i+1]]])
        if rot_global is None:
            rot_global = rot_i * norm(vector_i_plus_1 - vector_i)
        else:
            rot_global += rot_i * norm(vector_i_plus_1 - vector_i)

    return rot_global