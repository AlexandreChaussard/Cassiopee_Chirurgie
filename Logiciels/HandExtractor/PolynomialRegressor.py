import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from sklearn.preprocessing import PolynomialFeatures
from sklearn.linear_model import LinearRegression

from scipy import interpolate

def polynomial_regressor(x, y, z, pas_render=400):
    entries = [x, y, z]
    entries = np.atleast_1d(entries)
    idim, m = entries.shape
    if m <= 3:
        return [],[],[]
    tck, u = interpolate.splprep(entries, s=2)
    u_fine = np.linspace(0, 1, pas_render)
    x_fine, y_fine, z_fine = interpolate.splev(u_fine, tck)

    return x_fine, y_fine, z_fine

def polynomial_regressor_print(x, y, z, pas_render=200):
    tck, u = interpolate.splprep([x, y, z], s=2)
    x_knots, y_knots, z_knots = interpolate.splev(tck[0], tck)
    u_fine = np.linspace(0, 1, pas_render)
    x_fine, y_fine, z_fine = interpolate.splev(u_fine, tck)

    fig2 = plt.figure(2)
    ax3d = fig2.add_subplot(111, projection='3d')
    ax3d.plot(x, y, z, 'r*')
    ax3d.plot(x_knots, y_knots, z_knots, 'go')
    ax3d.plot(x_fine, y_fine, z_fine, 'g')
    fig2.show()
    plt.show()

def polynome(coefs=[0, 1, 1, 1, 1, 1, 1, 1, 1, 1], length=10, count=10):
    x,y,z = np.linspace(-length, length, count),np.linspace(-length, length, count),np.linspace(-length, length, count)
    polynome_x,polynome_y,polynome_z = [],[],[]
    for i in range(0, len(x)):
        polynome_x.append(coefs[0] +
                          coefs[1] * x[i] +
                          coefs[8] * y[i] * z[i] +
                          coefs[7] * x[i] ** 2)
        polynome_y.append(coefs[0] +
                          coefs[2] * y[i] -
                          coefs[5] * x[i] * z[i] +
                          coefs[8] * y[i] ** 2)
        polynome_z.append(coefs[0] +
                          coefs[3] * z[i] +
                          coefs[4] * x[i] * y[i] +
                          coefs[9] * z[i] ** 2)
    return polynome_x,polynome_y,polynome_z


x,y,z = polynome(length=10000, count=100)
polynomial_regressor(x, y, z, 3)
