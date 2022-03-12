import cv2
import numpy as np


# Renvoie une image cv2 de la vidéo spécifié
def getCameraView(self, cameraSlot=2):
    """ Récupère l'image courante de la vidéo
    :param cameraSlot: slot de la caméra sur l'ordinateur (default = 0)
    :return: frame - image de la caméra
    """
    if self.cap is None:
        self.cap = cv2.VideoCapture(cameraSlot, cv2.CAP_DSHOW)
    _, frame = self.cap.read()
    return frame