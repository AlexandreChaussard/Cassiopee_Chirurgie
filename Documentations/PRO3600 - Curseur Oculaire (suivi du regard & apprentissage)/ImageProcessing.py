import cv2
import numpy as np

"""
ImageProcessing regroupe l'ensemble des fonctions de traitement 
de l'image dans la récupération de l'oeil et de sa position
"""


def getPupilVector(lastPos, currentPos):
    """ Renvoie le vecteur déplacement de la pupille entre 2 images

    :param lastPos: dernière position de la pupille
    :param currentPos: position actuelle de la pupille
    :return: None
    """
    return [lastPos[0] - currentPos[0], lastPos[1] - currentPos[1]]


def getPupilPosition(image, thresholdValue=30):
    """ Renvoie la position de la pupille dans le cadre de détection

    :param image: image issue de la caméra
    :param thresholdValue: valeur de seuil de détection de la pupille
    :return: x, y - Position de la pupille | 0,0 si cas d'erreur
    """
    # Récupération de l'image de l'oeil seuillée adaptée
    threshold = getThresholdedEye(image, thresholdValue)

    # attente d'une erreur de format CV2 due à une non détection de l'oeil (mauvais seuillage généralement)
    try:
        # Recherche des contours de l'oeil
        contours = cv2.findContours(np.array(threshold), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        # Conditions de détection de l'oeil
        if contours is None:
            print("No eye contour detected")
            return [0, 0]
        if len(contours) == 0:
            print("No eye contour detected")
            return [0, 0]

        # Récupération des coordonnées de la pupille
        (x, y, w, h) = cv2.boundingRect(contours[0])

        return x + int(w / 2), y + int(h / 2)

    except cv2.error:
        # Retourne le cas d'erreur
        return 0, 0


def getThresholdedEye(image, thresholdValue):
    """ Permet de seuiller en noir/blanc l'imagette de l'oeil extraite d'une image caméra sur un critère de luminosité

    :param image: image issue de la caméra
    :param thresholdValue: valeur de seuil de détection de la pupille
    :return: threshold - Image de l'oeil sur laquelle est appliquée le seuil | [0, 0] cas d'erreur
    """
    # Extraction de l'imagette de l'oeil supérieur droit détecté
    image = extractEyesPicture(image)
    # Condition de détection
    if image is None:
        print("Eye_color is None")
        return [0, 0]

    # Passage en noir et blanc pour la réduction d'information et une meilleure détection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Récupération de la taille de l'image
    rows, cols = gray.shape
    # Application d'un flou gaussien
    gray_blurred = cv2.GaussianBlur(gray, (7, 7), 0)
    # Seuillage
    _, threshold = cv2.threshold(gray_blurred, thresholdValue, 255, cv2.THRESH_BINARY_INV)

    return threshold


def extractEyesPicture(image):
    """ Extrait une imagette de l'oeil supérieur droit

    :param image: image type openCV2 issue de la caméra
    :return: extracted - Imagette de l'oeil supérieur droit extrait
    """
    # Méthode des ondelettes de Haar pour la détection des yeux
    eye_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_eye.xml')

    # Définiton de l'image du visage en couleur
    roi_color, w, h = extractFacesPicture(image);
    # Condition de détection du visage
    if roi_color is None:
        print("roi_color is None")
        return None
    # Passage en noir et blanc pour la réduction d'information et une meilleure détection
    gray = cv2.cvtColor(roi_color, cv2.COLOR_BGR2GRAY)
    # Détection des yeux
    eyes = eye_cascade.detectMultiScale(gray)

    # Définition de l'image extraite
    extracted = None
    # Bouclage sur les yeux détectés
    for (ex, ey, ew, eh) in eyes:
        # Condition de détection de l'oeil supérieur droit
        if ex < w / 2 - 50 and ey < h / 2 + 50:
            extracted = roi_color[ey:ey + eh, ex:ex + ew]

    return extracted


def extractFacesPicture(image):
    """ Extrait une image englobant le visage de l'utilisateur

    :param image: image type openCV2 issue de la caméra
    :return: extracted - Image englobant le visage de l'utilisateur
    """
    # Méthode des ondelettes de Haar pour la détection de visage
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    # Passage en noir et blanc pour la réduction d'information et une meilleure détection
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # Détection des visages
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    # Conditions de détection du visage
    if faces is None:
        print("No face detected")
        return None, None, None
    if len(faces) == 0:
        print("No face detected")
        return None, None, None
    # Extraction des données sur l'image du premier visage détecté
    (x, y, w, h) = faces[0]
    # Extraction du 1er visage détecté sur l'image en couleur
    extracted = image[y:y + h, x:x + w]
    return extracted, w, h


def showImage(image, imageName="noName"):
    """ Permet d'afficher à l'écran une image openCV2

    :param image: image à afficher
    :param imageName: nom de la fenêtre d'affichage
    :return: None
    """
    cv2.imshow(imageName, np.array(image))
    cv2.moveWindow(imageName, 900, 420);
