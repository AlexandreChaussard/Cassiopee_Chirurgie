import pyautogui
import ImageProcessing
import numpy as np
import Interface
from RoundButton import RoundButton
import tkinter as tk
import matplotlib
import cv2
import sys

matplotlib.use("TkAgg")
from matplotlib import pyplot as plt
from matplotlib.widgets import Button as mButton

"""
CursorScaling permet l'étalonnage du système
et le contrôle de cette phase
"""


class CursorScaling:

    # Constructeur de CursorScaling
    def __init__(self):
        """Constructeur de CursorScaling.

            lastPupilPosition : Donne le dernier vecteur position de l'oeil calculé
            approximation : Donne l'approximation calculée lors de l'échellonnage
            buttonsLocations : Liste des positions des points d'échelonnage sur l'écran
            registeredApproximations : Liste des position de la pupille enregistrés lors de l'échelonnage avec les positions des points cibles
            isThresholded : Booléan indiquant la validation de l'étape de seuillage
            eyeThreshold : Valeur du seuillage en luminosité pour définir le seuil de détection de l'oeil
            cap : Instance de la caméra
            fenetre : Instance de la fenêtre d'étalonnage
        """
        pass
        # Donne le dernier vecteur position de l'oeil calculé
        self.lastPupilPosition = [0, 0]

        # Donne l'approximation calculée lors de l'échellonnage
        self.approximation = []

        # Liste des positions des points d'échelonnage sur l'écran
        self.buttonsLocations = [[0, 0], [0, 30], [0, 60]]

        # Liste des position de la pupille
        # enregistrés lors de l'échelonnage avec les positions des points cibles
        self.registeredApproximations = []

        # Booléan indiquant la validation de l'étape de seuillage
        self.isThresholded = False

        # Valeur du seuillage en luminosité pour définir le seuil de détection de l'oeil
        self.eyeThreshold = 10

        # Booléan indiquant si l'on est en mode étalonnage ou non
        self.isScaling = True

        # Instance de la caméra
        self.cap = None

        # Instance de la fenêtre d'étalonnage
        self.fenetre = None

    # Renvoie une image cv2 de la caméra
    def getCameraView(self, cameraSlot=2):
        """ Récupère l'image capturée par la caméra
        :param cameraSlot: slot de la caméra sur l'ordinateur (default = 0)
        :return: frame - image de la caméra
        """
        if self.cap is None:
            self.cap = cv2.VideoCapture(cameraSlot, cv2.CAP_DSHOW)
        _, frame = self.cap.read()
        return frame

    # Applique la position au curseur vis-à-vis du vecteur
    # déplacement de la pupille
    def setCursorPosition(self, vector):
        """ Applique la position au curseur au vecteur donnée sur l'écran

        :param vector: position où mettre le curseur sur l'écran
        :return: None
        """
        pyautogui.moveTo(vector[0], vector[1])

    # Constitue l'hypothèse de régression
    # sur l'écran étalonné les valeurs étalons
    # et optimisée
    # theta défini le vecteur de paramétrisation
    # x défini le vecteur d'entrer nouvelle
    def hypothesis(self, theta, x):
        """ Fonction hypothèse de la régression linéaire

        :param theta: vecteur paramètre de la régression
        :param x: position de l'oeil entrante (X ou Y)
        :return: y - Position estimée sur l'écran
        """
        # On définie le vecteur sortie supposé
        y = 0
        if True:
            return theta[0] + theta[1] * x
        # On construit y = sum(theta_i*x_i)
        for i in range(0, len(x)):
            y = theta[i] * x[i]
        return y

    # Enregistre le point d'étalonnage en utilisation
    # la dernière position de la pupille
    def pointClickEvent(self, button):
        """ Définie les actions liées au clic sur les boutons d'étalonnage

        :param button: bouton sur lequel est effectué le clic
        :return: None
        """
        # On récupère les coordonnées du curseur
        mouseX, mouseY = pyautogui.position()

        # On récupère les coordonnées de la pupille
        eyeX, eyeY = ImageProcessing.getPupilPosition(self.getCameraView(), self.eyeThreshold)
        print("Position de l'oeil : " + str(eyeX) + ", " + str(eyeY))
        # Condition de détection de la pupille
        if eyeX == 0 and eyeY == 0:
            return
        # On enregistre la réalisation d'étalonnage en prévision de la régression
        self.registeredApproximations.append([mouseX, mouseY, eyeX, eyeY])
        # On supprime le bouton cliqué si tout a bien marché
        button.destroy()

        # Condition définissant que tous les boutons ont été cliqués
        if len(self.registeredApproximations) == len(self.buttonsLocations):

            # Construction des matrice échantillon :
            # échantillons d'entrée : eyeX, eyeY
            XX = []
            XY = []
            # échantillons de sortie : mouseX, mouseY
            YX = []
            YY = []
            simpleVecEyeX = []
            simpleVecEyeY = []
            for i in range(0, len(self.registeredApproximations)):
                simpleVecEyeX.append(self.registeredApproximations[i][2])
                simpleVecEyeY.append(self.registeredApproximations[i][3])
                XX.append([1, self.registeredApproximations[i][2]])
                XY.append([1, self.registeredApproximations[i][3]])
                YX.append(self.registeredApproximations[i][0])
                YY.append(self.registeredApproximations[i][1])

            # Transformation matricielle puis transposition pour coller à la formule de l'équation normale
            XX = np.array(XX)

            XY = np.array(XY)

            YX = np.array(YX)
            YY = np.array(YY)

            print("XX : \n", XX)
            print("\nYX : \n", YX)

            # Détermination des paramètres optimales pour les régressions
            invertMatrixX = np.linalg.inv((XX.transpose()).dot(XX))
            invertMatrixY = np.linalg.inv((XY.transpose()).dot(XY))

            thetaX_ = np.matmul(invertMatrixX, ((XX.transpose()).dot(YX)))
            thetaY_ = np.matmul(invertMatrixY, ((XY.transpose()).dot(YY)))

            # Enregistrement des vecteurs optimisés
            self.approximation = [thetaX_, thetaY_]

            # On supprime la fenêtre étalonnage
            if self.fenetre is not None:
                self.fenetre.destroy()

            fig, axs = plt.subplots(2, 2)
            fig.suptitle("Etape 3 - Vérification de l'étalonnage", fontsize=12)
            axs[0, 0].plot(simpleVecEyeX, YX, 'ro')
            axs[0, 0].set_title('mouseX / EyeX')
            axs[0, 1].plot(simpleVecEyeY, YY, 'bo')
            axs[0, 1].set_title('mouseY / EyeY')

            axs[1, 0].plot(simpleVecEyeX, YX, 'ro')
            axs[1, 1].plot(simpleVecEyeY, YY, 'bo')

            minX = simpleVecEyeX[0]
            maxX = simpleVecEyeX[0]
            for i in simpleVecEyeX:
                if minX > i:
                    minX = i
                if maxX < i:
                    maxX = i
            x1 = np.linspace(minX, maxX, 400)
            minX = simpleVecEyeY[0]
            maxX = simpleVecEyeY[0]
            for i in simpleVecEyeY:
                if minX > i:
                    minX = i
                if maxX < i:
                    maxX = i
            x2 = np.linspace(minX, maxX, 400)

            By1 = thetaX_[0] + thetaX_[1] * x1
            By2 = thetaY_[0] + thetaY_[1] * x2

            axs[0, 0].plot(x1, By1)
            axs[0, 1].plot(x2, By2)

            ax1 = plt.axes([0.03, 0.02, 0.09, 0.06])
            ax2 = plt.axes([0.81, 0.02, 0.16, 0.06])
            ax3 = plt.axes([0.44, 0.02, 0.09, 0.06])
            validationRegression = mButton(ax1, "Valider")
            refaireRegression = mButton(ax2, "Recommencer")
            quitReg = mButton(ax3, "Quitter")

            # Sous fonctions évenementielles

            def closePlot(event=None):
                # On ferme le plot
                plt.close(fig)
                # On clear matplotlib sinon il fatigue
                plt.cla()
                plt.clf()
                # On désactive le mode étalonnage
                self.isScaling = False
                # Une fois les opérations effectuées, on affiche les boutons de contrôle
                Interface.displayButtons(self)

            def relaunchRegression(event=None):
                # On ferme le plot
                plt.close(fig)
                # On clear matplotlib sinon il fatigue
                plt.cla()
                plt.clf()
                # On relance l'étalonnage
                self.launchCalibrating()

            def quit(event=None):
                # On ferme le plot
                plt.close('all')
                # On quitte le programme
                sys.exit(0)

            # Initialisation des events liés aux boutons
            validationRegression.on_clicked(closePlot)
            refaireRegression.on_clicked(relaunchRegression)
            quitReg.on_clicked(quit)

            # Création de références type "Dummy" pour que les boutons fonctionnent avec le fig.show()
            ax1._button = validationRegression
            ax2._button = refaireRegression
            ax3._button = quitReg

            # On affiche la figure de régression
            fig.show()

    # Liste les positions des boutons étalons et initialise buttonsLocations
    def setButtonsPosition(self, xmax, ymax):
        """ Liste les positions des boutons étalons et initialise buttonsLocations

        :param xmax: taille de la fenêtre en X
        :param ymax: taille de la fenêtre en Y
        :return:
        """
        side_width = 3
        diam = 100
        ray = diam // 2
        xmilieu = xmax // 2
        ymilieu = ymax // 2
        self.buttonsLocations = [[0, 0], [0, ymilieu - ray], [0, ymax - diam], [xmilieu - ray, 0],
                                 [xmilieu - ray, ymilieu - ray],
                                 [xmilieu - ray, ymax - diam], [xmax - diam, 0], [xmax - diam, ymilieu - ray],
                                 [xmax - diam, ymax - diam]]

    # Affiche les points d'étalonnage à l'écran
    def displayCalibratingPoints(self):
        """ Lance le mode étalonnage et affiche les points

        :return: None
        """
        # Appel d'une fenêtre tk
        self.fenetre = tk.Tk()
        # Mode fullscreen
        self.fenetre.attributes('-fullscreen', True)
        # Echap permet de quitter l'interface
        self.fenetre.bind('<Escape>', lambda e: self.fenetre.destroy())
        # Récupération des informations de l'écran
        width = self.fenetre.winfo_screenwidth()
        height = self.fenetre.winfo_screenheight()
        # création de la fenêtre
        canvas = tk.Canvas(self.fenetre, width=width, height=height, bg='black')
        canvas.pack()
        # initialisation des positions des boutons étalons
        self.setButtonsPosition(width, height)
        # Placement des boutons
        for i in range(len(self.buttonsLocations)):
            button_i = RoundButton(self.fenetre, 100, 100, 50, 0, 'red', "black", self)
            button_i.place(x=self.buttonsLocations[i][0], y=self.buttonsLocations[i][1])
            # Ajout du bouton à la boucle tk
            button_i.pack

        # Lancement du scheduler tk
        self.fenetre.mainloop()

    # Affiche la vue seuillée de la caméra
    def runThresholdView(self):
        """ Affiche la vue seuillée de la caméra

        :return: None
        """
        # Tant que le seuillage n'est pas terminé
        while not self.isThresholded:
            # Récupération de l'image seuillée
            thresholdView = ImageProcessing.getThresholdedEye(self.getCameraView(), self.eyeThreshold)
            if thresholdView is not None:
                # Affichage de l'image seuillée

                ImageProcessing.showImage(thresholdView, "Etape 1 - Etalonnage du seuil")
                cv2.waitKey(20)

    # Affiche l'interface d'étalonnage du seuillage
    def displayThresholdCalibration(self):
        """ Affiche l'interface d'étalonnage du seuillage

        :return: None
        """
        # Appel d'une fenêtre tk
        self.fenetre = tk.Tk()
        self.fenetre.geometry("80x120+900+300")
        # Echap permet de quitter l'interface
        self.fenetre.bind('<Escape>', lambda e: self.fenetre.destroy())
        # Récupération des informations de l'écran
        width = self.fenetre.winfo_screenwidth()
        height = self.fenetre.winfo_screenheight()

        # création de la fenêtre

        # Permet la validation de l'étape de seuillage
        def validateThreshold():
            # On valide l'étape de seuillage
            self.isThresholded = True
            # On supprime toutes les fenêtres
            self.fenetre.destroy()
            cv2.destroyAllWindows()
            # On lance la calibration curseur en affichant les points de calibration
            self.displayCalibratingPoints()

        validate = tk.Button(self.fenetre, text='Valider', command=validateThreshold,
                             background="#494949", foreground="#F90808",
                             relief=tk.GROOVE, height=2, width=9, bd=4.55, font="serif", activebackground="#6B6B6B")
        validate.place(x=100, y=100)
        validate.grid()

        def updateThreshold(Event):
            self.eyeThreshold = scale.get()

        scale = tk.Scale(self.fenetre, from_=0, to=100, resolution=0.5, orient=tk.HORIZONTAL, background="#6B6B6B",
                         activebackground="#6B6B6B", foreground="#FFFFFF", highlightbackground="#494949",
                         command=updateThreshold)
        scale.bind("<Leave>", updateThreshold)
        scale.set(self.eyeThreshold)
        scale.place(x=0, y=60)

        # Lancement du scheduler tk
        self.fenetre.mainloop()

    def quitProcess(self):
        """ Permet de quitter le programme proprement

        :return: None
        """
        # On ferme toutes les fenêtre tkinter
        self.fenetre.destroy()
        # Ferme le flux caméra
        self.cap.release()
        # On coupe le programme
        sys.exit(0)

    # Lance le mode étalonnage
    def launchCalibrating(self):
        """ Lance le mode étalonnage

        :return: None
        """
        # On coupe les fenêtres tkInter dans le cas d'un réétalonnage
        if self.fenetre is not None:
            try:
                self.fenetre.destroy()
            except tk.TclError:
                None
        # On montre au programme qu'il est en mode étalonnage
        self.isScaling = True
        # On reset l'état du thresholding
        self.isThresholded = False
        # On reset les anciennes données de régression
        self.registeredApproximations.clear()

        # On affiche l'étape de seuillage
        self.displayThresholdCalibration()
