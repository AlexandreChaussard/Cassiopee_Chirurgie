import math
import scipy.stats
from fonctions_TP_python import * 

# Nombre de particules
N = 50
# Nombre de couleurs dans l'histogramme
N_b = 10
# Variable de discrimination des particules par l'histogramme de couleur associé
lamb = 20
# Valeurs de la matrice de bruit pour la variable aléatoire U
C1 = 300
C2 = 300

# On charge la 1ère image
im, filenames, T, SEQUENCE = lecture_image()
# On sélectionne la zone à suivre
zoneAT = selectionner_zone()

# On définit les dimensions de l'image extraite
h_width = zoneAT[2]
h_high = zoneAT[3]


# Permet d'initialiser les particules
def init_particles(sigma, mu):
    return sigma * np.random.randn(N, 2) + mu


# On initialise les particules
particles = init_particles(math.sqrt(300), [zoneAT[0], zoneAT[1]])


# Définie la distance BH entre deux histogrammes
def D(q, q_prime):
    somme = 0

    for i in range(0, N_b):
        somme = math.sqrt(q[i] * q_prime[i])

    return math.sqrt(1 - somme)


# Loi de y sachant x selon les histogrammes
def g(q, q_prime):
    return math.exp(- lamb * (D(q, q_prime) ** 2))


# On calcule l'histogramme de référence, en supposant qu'il n'évolue pas beaucoup lors du suivi
q_img, q_kmeans, q_histo_original = calcul_histogramme(im, zoneAT, N_b)
plt.pause(0.01)


# Fonction de filtrage particulaire
def filtrage_particulaire():
    X_est = particles  # initialisation bruitée, vecteur € R^Nx1
    estimated_trajectory_X = []  # initialisation du tableau des X estimés
    estimated_trajectory_Y = []  # initialisation du tableau des Y estimés
    N_eff_list = [] # initialisation de la liste des N_eff

    w = np.array([1 / N] * N).reshape(N, 1)  # matrice des poids, initialement uniformes

    X_t = X_est  # X_0 correspond aux particules initiales

    # On plot les particules
    for i in range(0, N):
        plt.plot(X_t[i][0], X_t[i][1], marker='x', color='blue')

    plt.pause(0.01)

    # On parcourt les images enregistrées
    for t in range(1, T):

        # Application de la loi de transition -> on propage les particules
        U = math.sqrt(C1) * np.random.randn(N, 2)
        X_t = X_t + U  # application du modèle

        W_t = []  # On prépare la liste des poids à l'instant t

        # On récupère l'image de l'instant t
        new_img = Image.open((SEQUENCE + filenames[t]))
        for i in range(0, N):
            rect_x = X_t[i][0]
            rect_y = X_t[i][1]
            q_prime_img, q_prime_kmeans, q_prime_histo = calcul_histogramme(new_img,
                                                                            [rect_x, rect_y, h_width, h_high],
                                                                            q_kmeans)

            w_value = w[i][-1] * g(q_histo_original, q_prime_histo)  # On calcule le poids de la particule
            W_t.append(w_value)

        W_t = np.array(W_t)
        W_t = W_t / np.sum(W_t)  # On normalise les poids

        N_eff_inv = 0 # On prépare le calcul de N_eff
        for i in range(0, N):
            w_value = W_t[i]
            N_eff_inv += w_value**2

        N_eff_list.append(1 / N_eff_inv)

        indice = np.random.choice(N, N, p=W_t)  # tire N particules selon la pondération W_t

        # rééchantillonnage
        X_t = X_t[indice]  # On récupère depuis les indices tirés un vecteur X_t rééchantillonés

        plt.cla()  # Efface le plot
        plt.clf()  # Efface la figure

        EX = 0  # Calcul de l'espérance en X
        EY = 0  # Calcul de l'espérance en Y

        for i in range(0, N):
            plt.plot(X_t[i][0], X_t[i][1], marker='x', color='blue')

            x_value = X_t[i][0]
            y_value = X_t[i][1]
            EX += x_value
            EY += y_value

        EX = EX / N
        EY = EY / N

        estimated_trajectory_X.append(EX + h_width/2)
        estimated_trajectory_Y.append(EY + h_high/2)

        X_est = np.hstack([X_est, X_t])  # On ajoute X_t à la matrice X_estimé en dernière colonne

        W_t = W_t.reshape(W_t.shape[0], 1)
        w = np.hstack([w, W_t])  # On ajoute W_t à la matrice des poids w

        # Plot les particules, le rectangle et la trajectoire
        plt.plot(estimated_trajectory_X, estimated_trajectory_Y, color="lime")
        plt.imshow(new_img)
        rect = ptch.Rectangle([EX, EY], h_width, h_high, linewidth=2, edgecolor='red', facecolor='None')
        plt.plot(EX, EY, marker='x', color='lime')
        currentAxis = plt.gca()
        currentAxis.add_patch(rect)

        plt.pause(0.01)

    return X_est, w, N_eff_list  # vecteurs de R^NxT


X_est, w, N_eff_list = filtrage_particulaire()

abscisse = []
for i in range(0, len(N_eff_list)):
    abscisse.append(i)

plt.cla()
plt.clf()

plt.title("N_eff en fonction de l'étape n du filtrage | lambda = " + str(lamb))
plt.plot(abscisse, N_eff_list)
plt.pause(100)
