import numpy as np
from PolynomialRegressor import *

def norm(vector):
    return np.linalg.norm(vector)


def vitesse_discret(trajectory):
    X = trajectory[0]
    Y = trajectory[1]
    Z = trajectory[2]

    list = []
    listNorm = []
    for i in range(0, len(X) - 1):
        v_i_x = X[i + 1] - X[i]
        v_i_y = Y[i + 1] - Y[i]
        v_i_z = Z[i + 1] - Z[i]
        v_i = [v_i_x, v_i_y, v_i_z]
        listNorm.append(norm(v_i))
        list.append(np.array(v_i))

    if list is None or listNorm is None or len(list) < 2 or len(listNorm) < 2:
        return None, None

    return list, listNorm


def acceleration_discret(trajectory):
    X = trajectory[0]
    Y = trajectory[1]
    Z = trajectory[2]

    list = []
    listNorm = []
    for i in range(0, len(X) - 2):
        acc_i_x = X[i + 2] - 2 * X[i + 1] + X[i]
        acc_i_y = Y[i + 2] - 2 * Y[i + 1] + Y[i]
        acc_i_z = Z[i + 2] - 2 * Z[i + 1] + Z[i]
        acc_i = [acc_i_x, acc_i_y, acc_i_z]
        listNorm.append(norm(acc_i))
        list.append(np.array(acc_i))

    if list is None or listNorm is None or len(list) < 2 or len(listNorm) < 2:
        return None, None

    return list, listNorm


def rotateur_discret(trajectory):
    matriceAcc, normAcc = acceleration_discret(trajectory)
    matriceV, normV = vitesse_discret(trajectory)

    list = []
    listNorm = []
    for i in range(0, len(matriceAcc)):
        acc = np.array(matriceAcc[i])
        v = np.array(matriceV[i])
        rotateur = np.cross(-acc, v)
        listNorm.append(norm(rotateur))
        list.append(rotateur)

    return list, listNorm


def rotateur_global(trajectory):
    listRot, listNorm = rotateur_discret(trajectory)
    return np.mean(listRot, axis=0)


def plot_rot_global(trajectory, axis=None, plotTrajectory=True, plotVitesse=True, plotAcceleration=True, plotMiniRot=True, multiplier=2):

    [x, y, z] = trajectory

    vitesses, vNorms = vitesse_discret(trajectory)
    accelerations, aNorms = acceleration_discret(trajectory)
    rotateurs, rNorms = rotateur_discret(trajectory)

    if axis is None:
        fig = plt.figure()
        axis = fig.gca(projection='3d')
        axis.set_xlabel('X')
        axis.set_ylabel('Y')
        axis.set_zlabel('Z')

    rot_global = rotateur_global(trajectory)
    rot_global = rot_global/norm(rot_global) * multiplier
    mean_vec = np.array([np.mean(x), np.mean(y), np.mean(z)])
    axis.plot([mean_vec[0], mean_vec[0] + rot_global[0]],
              [mean_vec[1], mean_vec[1] + rot_global[1]],
              [mean_vec[2], mean_vec[2] + rot_global[2]],
              color='k')
    axis.plot([mean_vec[0] + rot_global[0]],
              [mean_vec[1] + rot_global[1]],
              [mean_vec[2] + rot_global[2]],
              color='k',
              marker="o",
              label="Rotateur interpolé")

    if plotTrajectory:
        axis.plot(x, y, z, label="Trajectoire")

    for i in range(0, len(x) - 2):
        x_i, y_i, z_i = x[i], y[i], z[i]
        [v_x_i, v_y_i, v_z_i] = np.array([vitesses[i][0], vitesses[i][1], vitesses[i][2]]) * 100
        [acc_x_i, acc_y_i, acc_z_i] = np.array([accelerations[i][0], accelerations[i][1], accelerations[i][2]]) * 1000
        [rot_x_i, rot_y_i, rot_z_i] = np.array([rotateurs[i][0], rotateurs[i][1], rotateurs[i][2]]) * 10000

        if plotVitesse:
            axis.plot([x_i, x_i + v_x_i],
                      [y_i, y_i + v_y_i],
                      [z_i, z_i + v_z_i], color="blue", alpha=0.5)
        if plotAcceleration:
            axis.plot([x_i, x_i + acc_x_i],
                      [y_i, y_i + acc_y_i],
                      [z_i, z_i + acc_z_i], color="g", alpha=0.5)
        if plotMiniRot:
            axis.plot([x_i, x_i + rot_x_i],
                      [y_i, y_i + rot_y_i],
                      [z_i, z_i + rot_z_i], color="r", alpha=0.5)

    plt.legend()


#trajectory = polynome(length=10, count=300)
#plot_rot_global(trajectory)
#plt.show()
