import numpy as np

def rotationels_discret(trajectory):
    X = trajectory[0]
    Y = trajectory[1]
    Z = trajectory[2]

    list = []
    for i in range(0, len(X)-1):
        rot_i_x = ((Z[i+1]-Z[i])/(Y[i+1]-Y[i]) - (Y[i+1]-Y[i])/(Z[i+1]-Z[i]))
        rot_i_y = ((X[i+1]-X[i])/(Z[i+1]-Z[i]) - (Z[i+1]-Z[i])/(X[i+1]-X[i]))
        rot_i_z = ((Y[i+1]-Y[i])/(X[i+1]-X[i]) - (X[i+1]-X[i])/(Y[i+1]-Y[i]))
        rot_i = [rot_i_x, rot_i_y, rot_i_z]
        list.append(np.array(rot_i))

    return list

def norm(vect):
    return (vect[0]**2 + vect[1]**2 + vect[2]**2)**.5

def rotationnel_global(trajectory):
    X = trajectory[0]
    Y = trajectory[1]
    Z = trajectory[2]
    list_rot_discret = rotationels_discret(trajectory)

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