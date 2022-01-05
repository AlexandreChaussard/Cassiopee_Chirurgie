import pyautogui
from CursorScaling import CursorScaling
import ImageProcessing
import threading
import keyboard

"""qqq
Main correspond au programme principal à lancer pour lancer le programme
"""

# Définition du curseur étalon
scaler = CursorScaling()
# Dépacement de la sécurité grand mouvement
pyautogui.FAILSAFE = False


def start():
    """ Fonction principale du programme
    :return: None
    """
    # Définition de la fonction de gestion du curseur
    while True:
        if keyboard.is_pressed('q'):
            scaler.quitProcess()
        # Si l'on est en attente du seuillage
        if not scaler.isThresholded:
            # Lancement de l'affichage seuillée de l'oeil
            scaler.runThresholdView()
        # Condition de mise à jour de la position du curseur
        if not scaler.isScaling:
            # On récupère la position de l'oeil
            [eyeX, eyeY] = ImageProcessing.getPupilPosition(scaler.getCameraView(), scaler.eyeThreshold)
            # On en déduit la position prévue du curseur Les index 0,1 références thetaX et thetaY optimisant
            # l'hypothèse de régression et ont été calculés lors de l'étalonnage
            pos = [scaler.hypothesis(scaler.approximation[0], eyeX), scaler.hypothesis(scaler.approximation[1], eyeY)]
            # On déplace le curseur à cette position
            if [eyeX, eyeY] != [0, 0]:
                scaler.setCursorPosition(pos)
            mouseX, mouseY = pyautogui.position()
            print("\neyeX : ", eyeX, " eyeY : ", eyeY, "threshold : ", scaler.eyeThreshold)
            print("predictedMouseX : ", pos[0], " predictedMouseY : ", pos[1])
            print("mouseX : ", mouseX, "mouseY : ", mouseY)
            # On enregistre le dernier vecteur position de la pupille
            scaler.lastPupilPosition[0], scaler.lastPupilPosition[1] = pos[0], pos[1]


threading.Thread(target=start).start()

# Lancement de l'étalonnage au démarrage du programme
scaler.launchCalibrating()

# Ferme le flux caméra
if scaler.cap is not None:
    scaler.cap.release()
