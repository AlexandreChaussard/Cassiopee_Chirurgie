# -*- coding: utf-8 -*-

import argparse
import os.path
import cv2
import numpy as np


parser = argparse.ArgumentParser(description="Lit la vidéo donnée en argument et renvoie une vidéo avec les "
                                             "annotations des mains et la posture détectée sur la vidéo. "
                                             "La vidéo doit être au formant .avi. \n "
                                             "Pour utiliser le programme sur une unique vidéo, tapez : | \n "
                                             "python main.py -i vid1.avi \n "
                                             "| Sachez que le programme accepte plusieurs vidéos en argument "
                                             "| python main.py -i vid1.avi vid2.avi vid3.avi | par exemple")

# On ajoute l'option (-i ou --input) qui permet de donner une vidéo (.avi) en argument
parser.add_argument("-i", "--input", nargs='+', type=str, help="Chemin vers la video. Si la vidéo est dans le même "
                                                               "répertoire que le programme, écrivez simplement : "
                                                               "python main.py -i 'nom_video'.avi")
args = parser.parse_args()


# Vérifications (existence d'au moins un paramètre et son format)
if not args.input:
    print("Aucune vidéo n'a été donnée en entré.")
    print("Utiliser --help pour des explications sur l'utilisation du programme")
    exit()
# Check if the given file have bag extension
for id, name in enumerate(args.input):
    if os.path.splitext(name)[1] != ".avi":
        print("Le format du fichier donné n° " + str(id + 1) + " n'est pas le bon.")
        print("Seul le format de vidéo .avi est accepté")
        print('Source : ' + str(name))
        exit()


