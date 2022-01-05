import numpy as np
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from PIL import Image
from fonctions_TP_python import *

N = 50
N_b = 10
lamb = 20
C1 = 300
C2 = 300
F = np.array([[1, 0],
              [0, 1]])

im, filenames, T, SEQUENCE = lecture_image()
zoneAT = selectionner_zone()

q_img, q_kmeans, q = calcul_histogramme(im, zoneAT, N_b)
print("histo 1")


def init_particles(sigma, mu):
    return sigma * np.random.randn(N, 2) + mu


particles = init_particles((300) ** .5, [zoneAT[0], zoneAT[1]])


def D(q, q_prime):
    somme = 0

    for i in range(0, len(q)):
        somme = (q[i] * q_prime[i]) ** .5

    return (1 - somme) ** .5


def g(q, q_prime):
    return np.exp(- lamb * D(q, q_prime) ** 2)


def filtrage_particulaire():
    X_est = particles  # vecteur € R^Nx1
    w = np.array([1/len(X_est)] * len(X_est)).reshape(1, len(X_est))  # vecteur des poids

    rememberZoneAT = zoneAT.copy()
    zoneAT_matrix = np.zeros((N, 4))
    zoneAT_matrix[:][2] = rememberZoneAT[2]
    zoneAT_matrix[:][3] = rememberZoneAT[3]

    print("debug 2")

    for t in range(1, T):

        indice = np.random.choice(range(0, 50), N, list(w[:, -1]))  # tire N particules selon la pondération w

        X_t_moins_1 = X_est[indice, :]
        X_t = X_t_moins_1 + np.random.randn(N,2) * np.array([C1, C2])   # application du modèle

        W_t = []

        img = Image.open((SEQUENCE + filenames[t]))
        print(SEQUENCE, filenames[t])
        print("Passé")
        for i in range(0, N):
            zoneAT_matrix[i][0] = X_est[i][0]
            zoneAT_matrix[i][1] = X_est[i][1]

            q_prime_img, q_prime_kmeans, q_prime = calcul_histogramme(img, zoneAT_matrix[i], N_b)
            W_t.append(g(q, q_prime))

        W_t = W_t / np.sum(W_t)
        X_est = np.hstack([X_est, X_t])

        w = np.hstack([w, W_t])

        plt.Rectangle(zoneAT[0:2], zoneAT[2], zoneAT[3])

        plt.imshow(img)

    return X_est, w  # vecteurs de R^NxT

filtrage_particulaire()