from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from PolynomialRegressor import *

def find_plan(x, y, z):
    pca = PCA(n_components=2)
    pca.fit(np.array([x, y, z]))

    acp = pca.components_
    print("Variances expliquées\n", pca.explained_variance_ratio_)
    print("Composantes principales :\n", pca.components_)
    u = acp[1]
    v = acp[2]
    print("U\n", u)
    print("V\n",v)
    return u,v


x = [0, 10, 4, 1]
y = [1, 1, 3, 50]
z = [0, 0, 0, 0]

x,y,z = polynome(length=2, count=100)

fig = plt.figure()
ax = fig.gca(projection='3d')
ax.set_xlabel('X')
ax.set_ylabel('Y')
ax.set_zlabel('Z')
ax.plot(x,y,z, label="brute")

u,v = find_plan(x,y,z)
u = u*10
v = v*10


mean_point = [np.mean(x), np.mean(y), np.mean(z)]
ax.plot([mean_point[0] - u[0][0], mean_point[0] + u[0][0]],
        [mean_point[1] - u[1][0], mean_point[1] + u[1][0]],
        [mean_point[2] - u[2][0], mean_point[2] + u[2]], label="u")
ax.plot([mean_point[0] - v[0][0], mean_point[0] + v[0][0]],
        [mean_point[1] - v[1][0], mean_point[1] + v[1][0]],
        [mean_point[2] - v[2][0], mean_point[2] + v[2][0]], label="v")
plt.legend()
plt.show()