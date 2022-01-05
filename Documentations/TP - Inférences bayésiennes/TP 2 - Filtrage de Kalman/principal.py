import numpy as np
import matplotlib.pyplot as plt

# ----------- 2

T_e = 1
T = 100
sigma_Q = 1
sigma_px = 1
sigma_py = 30

x_init = np.array([[3, 40, -4, 20]]).transpose()
x_kalm = x_init
P_kalm = np.eye(4)

F = np.array([[1, T_e, 0, 0],
              [0, 1, 0, 0],
              [0, 0, 1, T_e],
              [0, 0, 0, 1]])
Q = sigma_Q ** 2 * np.array([[T_e ** 3 / 3, T_e ** 2 / 2, 0, 0],
                             [T_e ** 2 / 2, T_e, 0, 0],
                             [0, 0, T_e ** 3 / 3, T_e ** 2 / 2],
                             [0, 0, T_e ** 2 / 2, T_e]])
H = np.array([[1, 0, 0, 0],
              [0, 0, 1, 0]])
R = np.array([[sigma_px ** 2, 0],
              [0, sigma_py ** 2]])


# ----------- 3

def creer_trajectoire(F, Q, x_init, T):
    traj = []

    x_previous = x_init.copy()
    for i in range(0, T):
        U = np.random.multivariate_normal([0, 0, 0, 0], Q).reshape((4, 1))
        real = np.matmul(F, x_previous) + U
        x_previous = real.copy()
        traj.append(real)

    return np.array(traj).transpose().reshape(4, T)


vecteur_x = creer_trajectoire(F, Q, x_init, T)


# ----------- 4

def creer_observations(H, R, vecteur_x, T):
    obs = []
    X_t = vecteur_x.copy().transpose()

    for i in range(0, T):
        X = np.array(X_t[i]).reshape(4, 1)
        V = np.random.multivariate_normal([0, 0], R).reshape((2, 1))
        Y = np.matmul(H, X) + V
        obs.append(Y)

    return np.array(obs).transpose().reshape(2, T)


vecteur_y = creer_observations(H, R, vecteur_x, T)


# ----------- 5

def tracer(vecteur_x, vecteur_y):
    x_x = vecteur_x[0]
    y_x = vecteur_x[2]
    x_y = vecteur_y[0]
    y_y = vecteur_y[1]

    fig, ax = plt.subplots()
    ax.plot(x_x, y_x, 'r--', label="Trajectoire réelle")
    ax.plot(x_y, y_y, 'b+', label="Trajectoire observée")
    ax.legend()

    plt.title("Trajectoire réelle contre trajectoire observée")
    plt.show()


tracer(vecteur_x, vecteur_y)


# ----------- 6

def filtre_de_kalman(F, Q, H, R, y_k, x_kalm_prec, P_kalm_prec):
    # Partie prédiction

    x_kalm_prediction = np.matmul(F, x_kalm_prec)
    P_kalm_prediction = Q + np.matmul(np.matmul(F, P_kalm_prec), F.transpose())

    # Partie mise à jour

    S = np.matmul(np.matmul(H, P_kalm_prediction), H.transpose()) + R
    K = np.matmul(np.matmul(P_kalm_prediction, H.transpose()), np.linalg.inv(S))

    X_kalm_k = x_kalm_prediction + np.matmul(K, y_k.reshape(2, 1) - np.matmul(H, x_kalm_prediction))
    P_kalm_k = np.matmul(np.eye(4) - np.matmul(K, H), P_kalm_prediction)

    return [X_kalm_k, P_kalm_k]


# ----------- 7

x_est = []
x_kalm_prec = x_kalm
P_kalm_prec = P_kalm
for y_k in vecteur_y.transpose():
    [X_kalm_k, P_kalm_k] = filtre_de_kalman(F, Q, H, R, y_k, x_kalm_prec, P_kalm_prec)

    x_kalm_prec = X_kalm_k
    P_kalm_prec = P_kalm_k

    x_est.append(np.random.multivariate_normal(X_kalm_k.reshape(1, 4).tolist()[0], P_kalm_k))

x_est = np.array(x_est)


# ----------- 8

def err_quadra(k, vecteur_x, x_est):
    diff = (vecteur_x.reshape(T, 4)[k] - x_est.reshape(T, 4)[k])

    err = np.dot(diff, diff)
    # err = np.matmul((vecteur_x[k] - x_est.transpose()[k]).transpose().reshape(T, 1), (vecteur_x.transpose()[k] - x_est.transpose()[k]))
    return err


def erreur_moyenne(vecteur_x, x_est, T):
    sum = 0

    for i in range(0, T):
        sum = err_quadra(i, vecteur_x, x_est) ** .5

    return sum / (T)

def erreur_moyenne_propose(vecteur_x, x_est, T):
    sum = 0

    for i in range(0, T):
        sum = err_quadra(i, vecteur_x, x_est) ** .5

    return sum / (T*max_y_value(vecteur_x))

def max_y_value(vecteur_x):
    return abs(sum(abs(vecteur_x[2])))

# ----------- 9 & 10

def tracer_estime(vecteur_x, vecteur_y, x_est, T):
    x_x = vecteur_x[0]
    y_x = vecteur_x[2]
    x_y = vecteur_y[0]
    y_y = vecteur_y[1]

    fig, ax = plt.subplots()
    ax.plot(x_x, y_x, 'r--', label="Trajectoire réelle")
    ax.plot(x_y, y_y, 'b+', label="Trajectoire observée")
    ax.plot(x_est.transpose()[0], x_est.transpose()[2], "k.", label="Trajectoire estimée")
    ax.legend()

    plt.title("Trajectoire réelle, observée et estimée - Erreur moyenne absolue : " + str(erreur_moyenne(vecteur_x, x_est, T)) + " ; Erreur moyenne relative : " + str(erreur_moyenne_propose(vecteur_x, x_est, T)))
    plt.show()

    #abscisse = []
    #for i in range(0, len(x_x)):
    #    abscisse.append(i)

    #fig, ax = plt.subplots()
    #ax.plot(abscisse, x_x, 'r--', label="X réelle")
    #ax.plot(abscisse, x_y, 'b+', label="X observée")
    #ax.plot(abscisse, x_est.transpose()[0], "k.", label="X estimée")
    #ax.legend()
    #plt.title("Trajectoire en X réelle, observée et estimée - Erreur moyenne absolue : " + str(
    #    erreur_moyenne(vecteur_x, x_est, T)) + " ; Erreur moyenne relative : " + str(
    #    erreur_moyenne_propose(vecteur_x, x_est, T)))
    #plt.show()

    #abscisse = []
    #for i in range(0, len(x_y)):
    #    abscisse.append(i)

    #fig, ax = plt.subplots()
    #ax.plot(abscisse, y_x, 'r--', label="Y réelle")
    #ax.plot(abscisse, y_y, 'b+', label="Y observée")
    #ax.plot(abscisse, x_est.transpose()[2], "k.", label="Y estimée")
    #ax.legend()

    #plt.title("Trajectoire en Y réelle, observée et estimée - Erreur moyenne absolue : " + str(
    #    erreur_moyenne(vecteur_x, x_est, T)) + " ; Erreur moyenne relative : " + str(
    #    erreur_moyenne_propose(vecteur_x, x_est, T)))
    #plt.show()


tracer_estime(vecteur_x, vecteur_y, x_est, T)

######---------- | Application | ----------######

# ----------- 1

# On peut faire une moyenne entre la dernière valeur captée et la précédante

# ----------- 2

import scipy.io as scipyio


def filtre_de_kalman_avion(F, Q, H, R, y_k, x_kalm_prec, P_kalm_prec):
    # Partie prédiction

    x_kalm_prediction = np.matmul(F, x_kalm_prec)
    P_kalm_prediction = Q + np.matmul(np.matmul(F, P_kalm_prec), F.transpose())

    # Partie mise à jour

    S = np.matmul(np.matmul(H, P_kalm_prediction), H.transpose()) + R
    K = np.matmul(np.matmul(P_kalm_prediction, H.transpose()), np.linalg.inv(S))

    X_kalm_k = x_kalm_prediction + np.matmul(K, y_k.reshape(2, 1) - np.matmul(H, x_kalm_prediction))
    P_kalm_k = np.matmul(np.eye(4) - np.matmul(K, H), P_kalm_prediction)

    return [X_kalm_k, P_kalm_k, x_kalm_prediction, P_kalm_prediction]


vecteur_x_avion_ligne_dic = scipyio.loadmat("vecteur_x_avion_ligne.mat")
vecteur_x_avion_voltige_dic = scipyio.loadmat("vecteur_x_avion_voltige.mat")
vecteur_y_avion_ligne_dic = scipyio.loadmat("vecteur_y_avion_ligne.mat")
vecteur_y_avion_voltige_dic = scipyio.loadmat("vecteur_y_avion_voltige.mat")

vecteur_x_avion_ligne = []
for value in vecteur_x_avion_ligne_dic.values():
    if type(value) != np.ndarray:
        continue
    for y in value:
        vecteur_x_avion_ligne.append(y)
vecteur_x_avion_ligne = np.array(vecteur_x_avion_ligne)

vecteur_x_avion_voltige = []
for value in vecteur_x_avion_voltige_dic.values():
    if type(value) != np.ndarray:
        continue
    for y in value:
        vecteur_x_avion_voltige.append(y)
vecteur_x_avion_voltige = np.array(vecteur_x_avion_voltige)

vecteur_y_avion_ligne = []
for value in vecteur_y_avion_ligne_dic.values():
    if type(value) != np.ndarray:
        continue
    for y in value:
        vecteur_y_avion_ligne.append(y)
vecteur_y_avion_ligne = np.array(vecteur_y_avion_ligne)

vecteur_y_avion_voltige = []
for value in vecteur_y_avion_voltige_dic.values():
    if type(value) != np.ndarray:
        continue
    for y in value:
        vecteur_y_avion_voltige.append(y)
vecteur_y_avion_voltige = np.array(vecteur_y_avion_voltige)

if True:

    def tracer_trajectoire(vecteur_x, vecteur_y):
        x_est = []
        x_kalm_prec = x_kalm
        P_kalm_prec = P_kalm

        y_last = [0, 0]
        for y_k in vecteur_y.transpose():

            if str(y_k[0]) == "nan" or str(y_k[1]) == "nan":
                x_k = np.random.multivariate_normal(y_last[0].reshape(1, 4).tolist()[0], y_last[1])
                x_est.append(x_k)
                continue

            [X_kalm_k, P_kalm_k, m, P] = filtre_de_kalman_avion(F, Q, H, R, y_k, x_kalm_prec, P_kalm_prec)

            x_kalm_prec = X_kalm_k
            P_kalm_prec = P_kalm_k
            y_last = [m, P]
            x_est.append(np.random.multivariate_normal(X_kalm_k.reshape(1, 4).tolist()[0], P_kalm_k))

        x_est = np.array(x_est)
        tracer_estime(vecteur_x, vecteur_y, x_est, T)

    tracer_trajectoire(vecteur_x_avion_ligne, vecteur_y_avion_ligne)
    tracer_trajectoire(vecteur_x_avion_voltige, vecteur_y_avion_voltige)


######---------- | Partie 2 | ----------######

# ----------- 1

def cylindric(p_x, p_y):
    r = (p_x ** 2 + p_y ** 2) ** 0.5
    theta = np.arctan(p_y / p_x)

    return [theta, r]


# ----------- 2

def H(X):
    p_x = X[0][0]
    p_y = X[2][0]
    [theta, r] = cylindric(p_x, p_y)
    return np.array([[theta],
                     [r]])


# Que devient la loi g_k(y_k|x_k) ?

# ----------- 3

sigma_angle = np.pi / 180
sigma_dist = 10

R = np.array([[sigma_angle ** 2, 0],
              [0, sigma_dist ** 2]])


def creer_observation_radar(R, vecteur_x, T):
    obs = []
    X_t = vecteur_x.copy().transpose()

    for i in range(0, T):
        X = np.array(X_t[i]).reshape(4, 1)
        V = np.random.multivariate_normal([0, 0], R).reshape((2, 1))
        Y = H(X) + V
        obs.append(Y)

    return np.array(obs).transpose().reshape(2, T)


# ----------- 4
# Non car non linéaire

# ----------- 5

def f(X):
    return np.arctan(X[2][0] / X[0][0])


def g(X):
    return (X[0][0] ** 2 + X[2][0] ** 2) ** 0.5


def y_k(x_predic, x_k):
    vector = np.array([[f(x_predic)],
                      [g(x_predic)]])

    v_k = np.random.multivariate_normal([0, 0], R).reshape((2, 1))

    return vector + np.matmul(H(x_predic), (x_k - x_predic)) + v_k


# ----------- 6

def H_tilde(X):
    x = X[0][0]
    y = X[2][0]

    return np.array([[-y / (x ** 2 * (1 + (y / x) ** 2)), 0, 1 / (x * (1 + (y / x) ** 2)), 0],

                     [x / ((x ** 2 + y ** 2) ** 0.5), 0, y / ((x ** 2 + y ** 2) ** 0.5), 0]])


def filtre_de_kalman_radar(F, Q, R, y_k, x_kalm_prec, P_kalm_prec):
    # Partie prédiction

    x_kalm_prediction = np.matmul(F, x_kalm_prec)
    P_kalm_prediction = Q + np.matmul(np.matmul(F, P_kalm_prec), F.transpose())

    H_tild = H_tilde(x_kalm_prediction)

    # Indication
    y_k_prime = y_k.reshape(2, 1)

    # Partie mise à jour

    S = np.matmul(np.matmul(H_tild, P_kalm_prediction), H_tild.transpose()) + R
    K = np.matmul(np.matmul(P_kalm_prediction, H_tild.transpose()), np.linalg.inv(S))

    X_kalm_k = x_kalm_prediction.reshape(4, 1) + np.matmul(K, (y_k_prime - H(x_kalm_prediction)).reshape(2, 1)).reshape(4, 1)
    P_kalm_k = np.matmul(np.eye(4) - np.matmul(K, H_tild), P_kalm_prediction)

    return [X_kalm_k, P_kalm_k]


vecteur_y = creer_observation_radar(R, vecteur_x, T)

x_est = []
x_kalm_prec = x_kalm
P_kalm_prec = P_kalm
for y_k in vecteur_y.transpose():
    [X_kalm_k, P_kalm_k] = filtre_de_kalman_radar(F, Q, R, y_k, x_kalm_prec, P_kalm_prec)

    x_kalm_prec = X_kalm_k
    P_kalm_prec = P_kalm_k

    x_est.append(np.random.multivariate_normal(X_kalm_k.reshape(1, 4).tolist()[0], P_kalm_k))

vecteur_y_car = []
for i in range(0, T):
    r = vecteur_y[1][i]
    theta = vecteur_y[0][i]
    vecteur_y_car.append([r*np.cos(theta), r*np.sin(theta)])

x_est = np.array(x_est)
vecteur_y_car = np.array(vecteur_y_car).transpose()

tracer_estime(vecteur_x, vecteur_y_car, x_est, T)

def tracer_estime_polaire(vecteur_x, vecteur_y, x_est, T):

    def angle(px, py):
        return np.arctan(py/px)
    def radius(px, py):
        return (px**2 + py**2)**.5

    X_pol = []
    Y_pol = []
    X_est_pol = []

    for i in range(0, len(vecteur_x[0])):
        X_pol.append([angle(vecteur_x[0][i], vecteur_x[2][i]),
                      radius(vecteur_x[0][i], vecteur_x[2][i])])
        Y_pol.append([angle(vecteur_y[0][i], vecteur_y[1][i]),
                      radius(vecteur_x[0][i], vecteur_x[1][i])])
        X_est_pol.append([angle(x_est.transpose()[0][i], x_est.transpose()[2][i]),
                      radius(x_est.transpose()[0][i], x_est.transpose()[2][i])])

    X_pol = np.array(X_pol).transpose()
    Y_pol = np.array(Y_pol).transpose()
    X_est_pol = np.array(X_est_pol).transpose()

    x_x = X_pol[1]
    y_x = X_pol[0]
    x_y = Y_pol[1]
    y_y = Y_pol[0]

    fig, ax = plt.subplots()
    ax.plot(x_x, y_x, 'r--', label="Trajectoire réelle")
    ax.plot(x_y, y_y, 'b+', label="Trajectoire observée")
    ax.plot(X_est_pol[1], X_est_pol[0], "k.", label="Trajectoire estimée")
    ax.legend()

    plt.title("Trajectoire réelle, observée et estimée en polaire - Erreur moyenne : " + str(erreur_moyenne(vecteur_x, x_est, T)) + " ; Erreur moyenne relative : " + str(erreur_moyenne_propose(vecteur_x, x_est, T)))
    plt.show()

tracer_estime_polaire(vecteur_x, vecteur_y_car, x_est, T)

# Rapport faire des points +++ plot avec coordonnées polaires : bruit homoskedastique (c en anglais)