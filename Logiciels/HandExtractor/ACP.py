from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PolynomialRegressor import *


def find_plan(x, y, z):
    pca = PCA(n_components=2)
    pca.fit(np.array([x, y, z]).T)

    acp = pca.components_
    u = acp[0] / np.linalg.norm(acp[0])
    v = acp[1] / np.linalg.norm(acp[1])
    return u, v


def find_normal(u, v):
    w = np.array(np.cross(u/np.linalg.norm(u), v/np.linalg.norm(v)))
    if np.dot(w, np.array([0,0,1])) < 0:
        w = -w
    return w

def find_base(trajectory):
    x, y, z = trajectory[0], trajectory[1], trajectory[2]

    u, v = find_plan(x, y, z)
    w = find_normal(u, v)
    return np.array([u, v, w])

def plot_referentiel(trajectory, axis=None, multiplier=10):
    x, y, z = trajectory[0], trajectory[1], trajectory[2]
    if axis is None:
        fig = plt.figure()
        axis = fig.gca(projection='3d')
        axis.set_xlabel('X')
        axis.set_ylabel('Y')
        axis.set_zlabel('Z')
        axis.plot(x, y, z, label="brute")

    [u, v, w] = find_base(trajectory)*multiplier

    mean_point = [np.mean(x), np.mean(y), np.mean(z)]
    axis.plot([mean_point[0] - u[0], mean_point[0] + u[0]],
            [mean_point[1] - u[1], mean_point[1] + u[1]],
            [mean_point[2] - u[2], mean_point[2] + u[2]], label="u", color='b')
    axis.plot([mean_point[0] - v[0], mean_point[0] + v[0]],
            [mean_point[1] - v[1], mean_point[1] + v[1]],
            [mean_point[2] - v[2], mean_point[2] + v[2]], label="v", color='g')
    axis.plot([mean_point[0], mean_point[0] + w[0]],
            [mean_point[1], mean_point[1] + w[1]],
            [mean_point[2], mean_point[2] + w[2]], label="w", color='r')
    plt.legend()

#plot_referentiel(polynome(length=10, count=300))
#plt.show()