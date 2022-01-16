import numpy as np
import matplotlib.pyplot as plt
import time

start_time = time.time()

# ----------- 3

Q = 10
R = 20
T = 50
N = 50


# Générer la trajectoire
def generer_trajectoire(T, Q):
    x_o = np.random.normal(0, 1)
    X = [x_o]

    for i in range(1, T):
        u_n = np.random.normal(0, Q)

        x_n = 0.5 * X[i - 1] + 25 * X[i - 1] / (1 + X[i - 1] ** 2) + 8 * np.cos(1.2 * i) + u_n
        X.append(x_n)

    return np.array(X)


# ----------- 4

# Générer les observations
def generer_observations(X, R):
    Y = []

    for i in range(0, len(X)):
        v_n = np.random.normal(0, R)

        y_n = X[i] ** 2 / 20 + v_n
        Y.append(y_n)

    return np.array(Y)


# ----------- Tracer graphe

def erreur_quadratic(X, E):
    sum = 0

    for i in range(0, len(X)):
        sum = sum + (X[i] - E[i]) ** 2

    return sum/T

# Plot les graphes
def tracer(X, Y, Z=None):
    abscisses = []
    for i in range(0, len(X)):
        abscisses.append(i)

    fig, ax = plt.subplots()
    ax.plot(abscisses, X, "r--", label="Trajectoire")
    ax.plot(abscisses, Y, "+", label="Observations")

    if Z is not None:
        ax.plot(abscisses, Z, "b-.", label="Estimée")

    ax.legend()

    if Z is not None:
        error = erreur_quadratic(X, Z)
        plt.title("Trajectoire, observation et estimée | erreur quadratique moyenne : " + str(error));
    else:
        plt.title("Trajectoire et observations")
    plt.show()


X = generer_trajectoire(T, Q)
Y = generer_observations(X, R)

print("--- %s seconds ---" % (time.time() - start_time))

tracer(X, Y)

# ----------- 5

from scipy import stats


# Fais un tirage selon f n | n-1
def tirage_f(x_n_prev, n, Q):
    return np.random.normal(0.5 * x_n_prev + 25 * x_n_prev / (1 + x_n_prev ** 2) + 8 * np.cos(1.2 * n), Q)


# Evalue f n | n-1 en x_n, x_n_prev
def f(x_n, x_n_prev, n, Q):
    return stats.norm.pdf(x_n, 0.5 * x_n_prev + 25 * x_n_prev / (1 + x_n_prev ** 2) + 8 * np.cos(1.2 * n), Q)


# Evalue g en y_n | x_n
def g(y_n, x_n):
    return stats.norm.pdf(y_n, x_n ** 2 / 20, R)


def filtrage_particulaire(Y, N):
    X_est = np.random.randn(N, 1)  # vecteur € R^Nx1
    w = g(Y[0], X_est)  # vecteur des poids
    w = w / np.sum(w)  # normalisation des poids

    for t in range(1, T):

        X_t_moins_1 = np.random.choice(list(X_est[:, -1]), N, list(w[:, -1])).reshape(-1, 1)  # tire N particules selon la pondération w
        X_t = 0.5 * X_t_moins_1 + 25 * X_t_moins_1 / (1 + X_t_moins_1 ** 2) + 8 * np.cos(1.2 * t) + Q**.5 *np.random.randn(N,
                                                                                                                    1)  # application du modèle
        w_t = g(Y[t], X_t)
        w_t = w_t / np.sum(w_t)
        X_est = np.hstack([X_est, X_t])
        w = np.hstack([w, w_t])

    return X_est, w  # vecteurs de R^NxT


def esperance(X, W):
    return (X * W).sum(0)


end_time = time.time()

X_est, W = filtrage_particulaire(Y, N)
E = esperance(X_est, W)

print("--- %s seconds ---" % (time.time() - end_time))

tracer(X, Y, E)

# EQM en fonction de N

T = 50
abscisse = []
error_results = []
for i in range(1, 100):
    N = i
    abscisse.append(i)
    error = 0

    for j in range(0, 100):
        X = generer_trajectoire(T, Q)
        Y = generer_observations(X, R)
        X_est, W = filtrage_particulaire(Y, N)
        E = esperance(X_est, W)
        error += erreur_quadratic(X, E)
    error = error/100
    error_results.append(error)

plt.title("EQM en fonction de N")
plt.plot(abscisse, error_results)
plt.show()

# Temps d'exec en fonction de N

abscisse = []
results = []
X = generer_trajectoire(T, Q)
Y = generer_observations(X, R)
for i in range(1, 1000):
    N = i
    abscisse.append(i)
    start_time = time.time()
    X_est, W = filtrage_particulaire(Y, N)
    E = esperance(X_est, W)

    spent = time.time() - start_time
    results.append(spent)

plt.title("Temps d'exécution en fonction de N")
plt.plot(abscisse, results)
plt.show()

# EQM en fonction de T

abscisse = []
error_results = []
for i in range(1, 300):
    T = i
    abscisse.append(i)
    X = generer_trajectoire(T, Q)
    Y = generer_observations(X, R)

    X_est, W = filtrage_particulaire(Y, N)
    E = esperance(X_est, W)

    error = erreur_quadratic(X, E)
    error_results.append(error)

plt.title("EQM en fonction de T")
plt.plot(abscisse, error_results)
plt.show()
