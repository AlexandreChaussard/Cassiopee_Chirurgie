## 1

from scipy.stats import norm
import numpy as np


# bruite le vecteur X avec un bruit gaussien indep.
def bruit_gauss2(X, cl1, cl2, m1, sig1, m2, sig2):
    Y = []

    for x in X:

        if x == cl1:
            Y.append(np.random.normal(loc=m1, scale=sig1))
        else:
            Y.append(np.random.normal(loc=m2, scale=sig2))

    return Y


## 2

# Construit le signal segmenté S en classant les données du signal bruité
def classif_gauss2(Y, cl1, cl2, m1, sig1, m2, sig2):
    S = []

    for y in Y:

        if norm.pdf(y, m1, sig1) > norm.pdf(y, m2, sig2):
            S.append(cl1)
        else:
            S.append(cl2)

    return S


## 2

import matplotlib.pyplot as plt


# Calcul du taux d'erreur
def taux_erreur(A, B):
    if len(A) != len(B):
        print("Impossible de comparer des signaux n'ayant pas le même nombre d'échantillons")
        return

    # Index des signaux différents
    i = 0

    for k in range(0, len(A)):
        if A[k] != B[k]:
            i += 1

    return i / len(A)


# Script première idée
def premiere_idee(m1, sig1, m2, sig2):
    # Chargement des données
    X = np.load("signal.npy")

    # Construction de l'abscisse
    abscisse = []
    for i in range(0, len(X)):
        abscisse.append(i)

    # Récupération des classes
    cl1, cl2 = np.unique(X)

    # Bruitage du signal
    Y = bruit_gauss2(X, cl1, cl2, m1, sig1, m2, sig2)

    # Segmentation
    S = classif_gauss2(Y, cl1, cl2, m1, sig1, m2, sig2)

    # Plot
    plt.plot(abscisse, X, 'r-')
    plt.plot(abscisse, Y, 'g.')
    plt.plot(abscisse, S, 'b.')

    plt.title("Taux d'erreur moyen : " + str(erreur_moyenne_MV(100, m1, sig1, m2, sig2)))

    plt.show()


## 3

# Calcul moyen du taux d'erreur
def erreur_moyenne_MV(T, m1, sig1, m2, sig2, toPlot=False, forceX=np.load("signal.npy")):
    # Somme du calul de la moyenne
    tau = 0

    # Calcul de l'erreur partielle pour le plot
    erreur_partielle = []
    abscisse = []

    # Chargement des données
    X = forceX

    # Récupération des classes
    cl1, cl2 = np.unique(X)

    for k in range(0, T):
        # Bruitage du signal
        Y = bruit_gauss2(X, cl1, cl2, m1, sig1, m2, sig2)

        # Segmentation
        S = classif_gauss2(Y, cl1, cl2, m1, sig1, m2, sig2)

        # Construction de la somme
        tau += taux_erreur(X, S)

        # Ajout du taux d'erreur partiel
        erreur_partielle.append(tau / (k + 1))
        abscisse.append(k + 1)

    if toPlot:
        # Plot de l'erreur partielle
        plt.plot(abscisse, erreur_partielle)
        plt.title(
            "Taux d'erreur cumulé ((" + str(m1) + "," + str(sig1) + ") -" + " (" + str(m2) + "," + str(sig2) + "))")
        plt.show()

    return tau / T


# Interprétation lorsque T devient grand :

## 5

# Test de la méthode avec les 6 signaux

# M1 = [120, 127, 127, 127, 127]
# M2 = [130, 127, 128, 128, 128]
# SIG1 = [1, 1, 1, 0.1, 2]
# SIG2 = [2, 5, 1, 0.1, 3]

# for k in range(0, len(M1)):
#    premiere_idee(M1[k], SIG1[k], M2[k], SIG2[k])
#    erreur_moyenne_MV(100, M1[k], SIG1[k], M2[k], SIG2[k], toPlot=True)

## -------------- TP 2 ----------------- ##

## 1

# Calcule la loi du processus X a priori à partir du signal d'origine X
def calc_probaprio(X, cl1, cl2):
    # Paramètres de l'estimateur de p = E(X1)
    n = 0

    for x in X:
        if x == cl1:
            n += 1

    p1 = n / len(X)
    p2 = 1 - p1

    return [p1, p2]


from scipy.stats import norm


# Classe les éléments du signal bruité suivant le critère du MAP
def MAP_MPM2(Y, cl1, cl2, p1, p2, m1, sig1, m2, sig2):
    S = []

    for y in Y:

        if p1 * norm.pdf(y, loc=m1, scale=sig1) > p2 * norm.pdf(y, loc=m2, scale=sig2):
            S.append(cl1)
        else:
            S.append(cl2)

    return S


## 2

# Calcul moyen du taux d'erreur
def erreur_moyenne_MAP(T, p1, p2, m1, sig1, m2, sig2, toPlot=False, forceX=np.load("signal.npy")):
    # Somme du calul de la moyenne
    tau = 0

    # Calcul de l'erreur partielle pour le plot
    erreur_partielle = []
    abscisse = []

    # Chargement des données
    X = forceX

    # Récupération des classes
    cl1, cl2 = np.unique(X)

    for k in range(0, T):
        # Bruitage du signal
        Y = bruit_gauss2(X, cl1, cl2, m1, sig1, m2, sig2)

        # Segmentation
        S = MAP_MPM2(Y, cl1, cl2, p1, p2, m1, sig1, m2, sig2)

        # Construction de la somme
        tau += taux_erreur(X, S)

        # Ajout du taux d'erreur partiel
        erreur_partielle.append(tau / (k + 1))
        abscisse.append(k + 1)

    if toPlot:
        # Plot de l'erreur partielle
        plt.plot(abscisse, erreur_partielle)
        plt.title(
            "Taux d'erreur cumulé ((" + str(m1) + "," + str(sig1) + ") -" + " (" + str(m2) + "," + str(sig2) + "))")
        plt.show()

    return tau / T


def test():
    M1 = [120, 127, 127, 127, 127]
    M2 = [130, 127, 128, 128, 128]
    SIG1 = [1, 1, 1, 0.1, 2]
    SIG2 = [2, 5, 1, 0.1, 3]

    # Chargement des données
    X = np.load("signal.npy")

    # Récupération des classes de X
    cl1, cl2 = np.unique(X)

    # Récupération de la loi de X à priori
    [p1, p2] = calc_probaprio(X, cl1, cl2)

    # Construction de l'axe des abscisses
    abscisse = []
    for i in range(0, len(X)):
        abscisse.append(i)

    for k in range(0, len(M1)):
        # Bruitage de l'échantillon
        Y = bruit_gauss2(X, cl1, cl2, M1[k], SIG1[k], M2[k], SIG2[k])

        # Classification
        S = MAP_MPM2(Y, cl1, cl2, p1, p2, M1[k], SIG1[k], M2[k], SIG2[k])

        # Plot
        plt.plot(abscisse, X, 'r-')
        plt.plot(abscisse, Y, 'g.')
        plt.plot(abscisse, S, 'b.')
        plt.title(
            "(" + str(k + 1) + ") Taux d'erreur moyen (LR): " + str(
                erreur_moyenne_MAP(100, p1, p2, M1[k], SIG1[k], M2[k], SIG2[k], forceX=X)))
        plt.show()


# Commentaire : l'apport à priori de la connaissance de la loi de X, diminue le taux d'erreur moyen.
# Faire le tableau de comparaison ^^

## 3

import numpy as np


# Simule un signal de taille n composantes indépendantes à valeurs dans {cl1, cl2} avec proba {p1, p2}
def X_simu(n, cl1, cl2, p1, p2):
    X = []

    for i in range(0, n):
        u = np.random.rand()

        if u < p1:
            X.append(cl1)
        else:
            X.append(cl2)

    return X


## 4


# Comparaison des deux méthodes
def comparaison(n, cl1, cl2, P1=[0.1, 0.2, 0.3, 0.4, 0.5]):
    # Construction de l'axe des abscisses
    abscisse = []
    for i in range(0, n):
        abscisse.append(i)

    M1 = [120, 127, 127, 127, 127]
    M2 = [130, 127, 128, 128, 128]
    SIG1 = [1, 1, 1, 0.1, 2]
    SIG2 = [2, 5, 1, 0.1, 3]

    for k in range(0, len(M1)):

        for p1 in P1:
            # Déduction de p2
            p2 = 1 - p1

            # Génération du signal
            X = X_simu(n, cl1, cl2, p1, 1 - p1)
            # Bruitage
            Y = bruit_gauss2(X, cl1, cl2, M1[k], SIG1[k], M2[k], SIG2[k])

            # Segmentation selon le max de vraisemblance
            S_MV = classif_gauss2(Y, cl1, cl2, M1[k], SIG1[k], M2[k], SIG2[k])
            # Segmentation selon la méthode bayésienne
            S_MAP = MAP_MPM2(Y, cl1, cl2, p1, p2, M1[k], SIG1[k], M2[k], SIG2[k])

            # Plot
            plt.plot(abscisse, X, 'r-')
            plt.plot(abscisse, Y, 'g.')
            plt.plot(abscisse, S_MV, 'y.')
            plt.plot(abscisse, S_MAP, 'b.')

            plt.title("(" + str(k + 1) + " | " + str(p1) + ") Erreur moyenne : MV - " + str(
                erreur_moyenne_MV(100, M1[k], SIG1[k], M2[k], SIG2[k], forceX=X)) + " | MAP - " + str(
                erreur_moyenne_MAP(100, p1, p2, M1[k], SIG1[k], M2[k], SIG2[k], forceX=X)))

            plt.show()


# Affiche tous les graphes avec 50 points
def test2():
    comparaison(50, 100, 200)


##-------------- TP 3 -----------------##

## 1

# Choisit aléatoirement la classe cl1 ou clé avec les proba p1 et p2
def tirage_classe2(p1, cl1, cl2):
    u = np.random.rand()

    if u < p1:
        return cl1
    else:
        return cl2


## 2

# Génère une réalisation d'une chaîne de Markov de longueur n avec une loi initial de P10 et P20
# de matrice de transition A et de classes cl1 et cl2
def genere_Chaine2(n, cl1, cl2, A, p10):

    X = []

    u = np.random.rand()

    if u < p10:
        X.append(cl1)
    else:
        X.append(cl2)

    for i in range(1, n):

        u = np.random.rand()

        if X[i-1] == cl1:
            if u < A[0][0]:
                X.append(cl1)
            else:
                X.append(cl2)
        else:
            if u < A[1][1]:
                X.append(cl2)
            else:
                X.append(cl1)

    return X


## 3

from markovchain import MarkovChain


# Génère une réalisation de X et affiche sa représentation
def graphe_chaine2(A, plot=True):
    X = genere_Chaine2(50, 100, 200, A, 0.3)

    if plot:
        abscisse = []
        for i in range(0, len(X)):
            abscisse.append(i)

        plt.plot(abscisse, X, "r-")
        plt.show()

        mc = MarkovChain(A, ["cl1", "cl2"])
        mc.draw("./markov-chain.png")

    return X


## 4
def graphe_chaine_bruite2(A, m1, sig1, m2, sig2, cl1, cl2, plot=True):
    X = graphe_chaine2(A, False)
    Y = bruit_gauss2(X, cl1, cl2, m1, sig1, m2, sig2)

    if plot:
        abscisse = []
        for i in range(0, len(X)):
            abscisse.append(i)
        plt.plot(abscisse, X, "r-")
        plt.plot(abscisse, Y, "b.")
        plt.show()

    return Y


def test4():
    M1 = [120, 127, 127, 127, 127]
    M2 = [130, 127, 128, 128, 128]
    SIG1 = [1, 1, 1, 0.1, 2]
    SIG2 = [2, 5, 1, 0.1, 3]

    graphe_chaine_bruite2(A=np.array([[0.2, 0.8],
                                      [0.4, 0.6]]),
                          m1=M1[0], sig1=SIG1[0],
                          m2=M2[0], sig2=SIG2[0],
                          cl1=100, cl2=200)


##------- TP 4 ----------##

## 1

# Construction d'une matrice Mat_f pour le calcul des proba forward et backward
def gauss2(Y, m1, sig1, m2, sig2):
    Mat_f = []

    for y in Y:
        f1 = norm.pdf(y, loc=m1, scale=sig1)
        f2 = norm.pdf(y, loc=m2, scale=sig2)

        Mat_f.append([f1, f2])

    return np.array(Mat_f)


## 2

# Calcul récursif des composantes de la matrice alfa par le processus forward
def forward2(Mat_f, n, A, p10):
    a1 = [Mat_f[0][0] * p10, Mat_f[0][1] * (1 - p10)]
    alfa = [a1]

    for z in range(1, n):

        sumprevious0 = 0
        sumprevious1 = 0
        for j in range(0, len(a1)):
            sumprevious0 = alfa[z - 1][j] * A[j][0] + sumprevious0
            sumprevious1 = alfa[z - 1][j] * A[j][1] + sumprevious1

        sumprevious00 = sumprevious0 * Mat_f[z][0]
        sumprevious11 = sumprevious1 * Mat_f[z][1]

        aBis = [sumprevious00, sumprevious11]
        alfa.append(aBis)

    return alfa


## 3

# Calcul récursif des composantes de la matrice betha par le processus backward
def backward2(Mat_f, n, A, p10):
    bethaN = [1, 1]
    betha = [bethaN]

    for z in range(1, n):

        sumprevious0 = 0
        sumprevious1 = 0
        for j in range(0, len(bethaN)):
            sumprevious0 = betha[z-1][j] * A[0][j] * Mat_f[n - z][j] + sumprevious0
            sumprevious1 = betha[z-1][j] * A[1][j] * Mat_f[n - z][j] + sumprevious1

        aBis = [sumprevious0, sumprevious1]
        betha.append(aBis)

    betha.reverse()

    return betha


## 4

# Segmente le signal par le critère MPM pour les chaines de markov cachées
def MPM_chaine2(Mat_f, n, cl1, cl2, A, p10):
    # Liste des sous-éléments segmentés
    S = []

    alfa = forward2(Mat_f, n, A, p10)
    betha = backward2(Mat_f, n, A, p10)
    for i in range(0, len(alfa)):
        c = alfa[i][0] * betha[i][0]
        d = alfa[i][1] * betha[i][1]

        if c > d:
            S.append(cl1)
        else:
            S.append(cl2)

    return S


## 5 & 8

def seg_chaines_MPM_super2(n, cl1, cl2, A, p10, m1, sig1, m2, sig2, plot=True, forceX=None, index=0):
    if forceX is None:
        X = genere_Chaine2(n=n, cl1=cl1, cl2=cl2, A=A, p10=p10)
    else:
        X = forceX
    Y = bruit_gauss2(X, cl1, cl2, m1, sig1, m2, sig2)

    Mat_f = gauss2(Y, m1, sig1, m2, sig2)

    S = MPM_chaine2(Mat_f, n, cl1, cl2, A, p10)

    tau = erreur_moyenne_MAP_chaine2(200, n, A, p10, m1, sig1, m2, sig2, toPlot=False, forceX=X, index=index)

    abscisse = []
    for i in range(0, len(X)):
        abscisse.append(i)

    if plot:
        abscisse = []
        for i in range(0, len(X)):
            abscisse.append(i)
        plt.plot(abscisse, X, "r-")
        plt.plot(abscisse, Y, "g.")
        plt.plot(abscisse, S, "b.")
        plt.title("("+ str(index) + ") Taux d'erreur (CM-MAP) : " + str(tau))
        plt.show()


# Calcul moyen du taux d'erreur
def erreur_moyenne_MAP_chaine2(T, n, A, p10, m1, sig1, m2, sig2, toPlot=False, forceX=np.load("signal.npy"), index=0):
    # Somme du calul de la moyenne
    tau = 0

    # Calcul de l'erreur partielle pour le plot
    erreur_partielle = []
    abscisse = []

    # Chargement des données
    X = forceX

    # Récupération des classes
    cl1, cl2 = np.unique(X)

    for k in range(0, T):
        # Bruitage du signal
        Y = bruit_gauss2(X, cl1, cl2, m1, sig1, m2, sig2)

        # Segmentation
        Mat_f = gauss2(Y, m1, sig1, m2, sig2)

        S = MPM_chaine2(Mat_f, n, cl1, cl2, A, p10)

        # Construction de la somme
        tau += taux_erreur(X, S)

        # Ajout du taux d'erreur partiel
        erreur_partielle.append(tau / (k + 1))
        abscisse.append(k + 1)

    if toPlot:
        # Plot de l'erreur partielle
        plt.plot(abscisse, erreur_partielle)
        plt.title(
            "("+ str(index)+ ") Taux d'erreur cumulé ((" + str(m1) + "," + str(sig1) + ") -" + " (" + str(m2) + "," + str(sig2) + "))")
        plt.show()

    return tau / T

## 6

def test6(n):
    M1 = [120, 127, 127, 127, 127]
    M2 = [130, 127, 128, 128, 128]
    SIG1 = [1, 1, 1, 0.1, 2]
    SIG2 = [2, 5, 1, 0.1, 3]
    A_ARRAY = []

    PREPARE_A = [0.1, 0.2, 0.3, 0.4, 0.5]
    PREPARE_A2 = [0.5, 0.4, 0.3, 0.2, 0.1]

    cl1, cl2 = 100,200
    p10 = 0.5

    for j in range(0, len(PREPARE_A)):
        i = PREPARE_A[j]
        k = PREPARE_A2[j]
        A_ARRAY.append(np.array([[i, 1 - i], [k, 1 - k]]))

    abscisse = []
    for i in range(0, n):
        abscisse.append(i)

    for i in range(0, len(A_ARRAY)):

        A = A_ARRAY[i]
        X = genere_Chaine2(n=n, cl1=cl1, cl2=cl2, A=A, p10=p10)

        for j in range(0, len(M1)):
            m1 = M1[j]
            m2 = M2[j]
            sig1 = SIG1[j]
            sig2 = SIG2[j]
            seg_chaines_MPM_super2(n, cl1, cl2, A, p10, m1, sig1, m2, sig2, plot=True, forceX=X, index=j+1)

            [p1,p2] = calc_probaprio(X, cl1, cl2)

            # Bruitage de l'échantillon
            Y = bruit_gauss2(X, cl1, cl2, M1[j], SIG1[j], M2[j], SIG2[j])

            # Classification
            S = MAP_MPM2(Y, cl1, cl2, p1, p2, M1[j], SIG1[j], M2[j], SIG2[j])

            # Plot
            plt.plot(abscisse, X, 'r-')
            plt.plot(abscisse, Y, 'g.')
            plt.plot(abscisse, S, 'b.')
            plt.title(
                "(" + str(j + 1) + ") Taux d'erreur moyen (MAP indep): " + str(
                    erreur_moyenne_MAP(100, p1, p2, M1[j], SIG1[j], M2[j], SIG2[j], forceX=X)))
            plt.show()

## 7

# Generateur de la matrice de transition
def calc_transit_prio2(X, n, cl1, cl2):

    metcl1 = False
    metcl2 = False

    indexCl1 = 0
    indexCl2 = 0
    nCl1 = 0
    nCl2 = 0
    taille = len(X)
    for x in X:
        if x == cl1:
            if metcl2:
                metcl2 = False
            if metcl1:
                indexCl1 += 1

            metcl1 = True
            nCl1 += 1
        else:
            if metcl1:
                metcl1 = False

            if metcl2:
                indexCl2 += 1

            metcl2 = True
            nCl2 += 1

    pCl1toCl1 = indexCl1/nCl1
    pCl2toCl2 = indexCl2/nCl2
    pCL1toCl2 = 1 - pCl1toCl1
    pCl2toCl1 = 1 - pCl2toCl2

    return np.array([[pCl1toCl1, pCL1toCl2],
                    [pCl2toCl1, pCl2toCl2]])

## 9

# Test sur les signaux 0 à 5
def testSignals():
    M1 = [120, 127, 127, 127, 127]
    M2 = [130, 127, 128, 128, 128]
    SIG1 = [1, 1, 1, 0.1, 2]
    SIG2 = [2, 5, 1, 0.1, 3]
    X_ARRAY_NAME = ["signal.npy", "signal1.npy", "signal2.npy", "signal3.npy", "signal4.npy", "signal5.npy"]
    X_ARRAY = []

    p10 = 0.5

    for name in X_ARRAY_NAME:
        X_ARRAY.append(np.load(name))

    for i in range(0, len(X_ARRAY)):

        X = X_ARRAY[i]
        cl1, cl2 = np.unique(X)
        A = calc_transit_prio2(X, len(X), cl1, cl2)

        abscisse = []
        for i in range(0, len(X)):
            abscisse.append(i)

        for j in range(0, len(M1)):
            m1 = M1[j]
            m2 = M2[j]
            sig1 = SIG1[j]
            sig2 = SIG2[j]
            seg_chaines_MPM_super2(len(X), cl1, cl2, A, p10, m1, sig1, m2, sig2, plot=True, forceX=X, index=j+1)

            [p1,p2] = calc_probaprio(X, cl1, cl2)

            # Bruitage de l'échantillon
            Y = bruit_gauss2(X, cl1, cl2, M1[j], SIG1[j], M2[j], SIG2[j])

            # Classification
            S = MAP_MPM2(Y, cl1, cl2, p1, p2, M1[j], SIG1[j], M2[j], SIG2[j])

            # Plot
            plt.plot(abscisse, X, 'r-')
            plt.plot(abscisse, Y, 'g.')
            plt.plot(abscisse, S, 'b.')
            plt.title(
                "(" + str(j + 1) + ") Taux d'erreur moyen (MAP indep): " + str(
                    erreur_moyenne_MAP(100, p1, p2, M1[j], SIG1[j], M2[j], SIG2[j], forceX=X)))
            plt.show()

testSignals()

## 10

## Que se passe-t-il lorsque la taille de la chaine augmente ?

## 11

# Programmation du rescaling
# Calcul récursif des composantes de la matrice alfa par le processus forward
def forward2_rescaled(Mat_f, n, A, p10):
    a1 = [Mat_f[0][0] * p10, Mat_f[0][1] * (1 - p10)]
    alfa = [a1]

    for z in range(1, n):

        sumprevious0 = 0
        sumprevious1 = 0
        for j in range(0, len(a1)):
            sumprevious0 = alfa[z - 1][j] * A[j][0] + sumprevious0
            sumprevious1 = alfa[z - 1][j] * A[j][1] + sumprevious1

        sumprevious00 = sumprevious0 * Mat_f[z][0]
        sumprevious11 = sumprevious1 * Mat_f[z][1]

        aBis = [sumprevious00, sumprevious11]
        alfa.append(aBis)

    return alfa


## 3

# Calcul récursif des composantes de la matrice betha par le processus backward
def backward2_rescaled(Mat_f, n, A, p10):
    bethaN = [1, 1]
    betha = [bethaN]

    for z in range(1, n):

        sumprevious0 = 0
        sumprevious1 = 0
        for j in range(0, len(bethaN)):
            sumprevious0 = betha[z-1][j] * A[0][j] * Mat_f[n - z][j] + sumprevious0
            sumprevious1 = betha[z-1][j] * A[1][j] * Mat_f[n - z][j] + sumprevious1

        aBis = [sumprevious0, sumprevious1]
        betha.append(aBis)

    betha.reverse()

    return betha