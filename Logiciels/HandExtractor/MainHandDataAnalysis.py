from HandData import HandData
import tkinter as tk
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
import matplotlib as mpl
import numpy as np
from mpl_toolkits.mplot3d import Axes3D


def chooseFile():
    tk.Tk().withdraw()
    return askopenfilename()


path = chooseFile()
if path == '':
    exit(0)

handData = HandData(path)
handData.load()

fig = plt.figure()
ax = fig.gca(projection='3d')
#ax = fig.add_subplot(111, projection='3d')

point = 4
for i in range(0, 21):

    x = handData.getX_aroundAnnotation(i, "Aiguille", point, 100)
    y = handData.getY_aroundAnnotation(i, "Aiguille", point, 100)
    z = handData.getZ_aroundAnnotation(i, "Aiguille", point, 100)

    x = x.reshape(1, -1)[0]
    y = y.reshape(1, -1)[0]
    z = z.reshape(1, -1)[0]

    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')
    ax.plot(x, y, z, label="Trajectoire " + str(i))
    ax.legend()

plt.show()
