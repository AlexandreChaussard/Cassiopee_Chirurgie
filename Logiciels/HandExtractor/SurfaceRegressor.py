import matplotlib.pyplot as plt
import numpy as np
import sklearn.linear_model
from PolynomialRegressor import *

from mpl_toolkits.mplot3d import Axes3D

x,y,z = polynome(coefs=[0, -1, -1, -1, -1, 1, 1, 1, 1, -1], length=5, count=300)

X_train = np.array([x, z]).transpose() #np.random.rand(2000).reshape(1000,2)*60
y_train = np.array(y)

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(X_train[:,0], X_train[:,1], y_train, marker='.', color='red')
ax.set_xlabel("X1")
ax.set_ylabel("X2")
ax.set_zlabel("y")

model = sklearn.linear_model.LinearRegression()
model.fit(X_train, y_train)
y_pred = model.predict(X_train)

coefs = model.coef_
intercept = model.intercept_
xs = np.tile(np.arange(61), (61,1))
ys = np.tile(np.arange(61), (61,1)).T
zs = xs*coefs[0]+ys*coefs[1]+intercept
print("Equation: y = {:.2f} + {:.2f}x1 + {:.2f}x2".format(intercept, coefs[0],
                                                          coefs[1]))

ax.plot_surface(xs,ys,zs, alpha=0.5)
plt.show()