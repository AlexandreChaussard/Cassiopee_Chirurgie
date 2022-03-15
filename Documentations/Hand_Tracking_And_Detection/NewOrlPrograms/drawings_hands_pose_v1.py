# -*- coding: utf-8 -*-

import time
import os
import cv2
import mediapipe as mp


def hands_pose_annotation(vid_name, do_hands_drawing=False, do_pose_drawing=False):

    # --------------------------------------------- #
    #           Initilisation de Médiapipe          #
    # --------------------------------------------- #

    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles

    # | Mains |
    mp_hands = mp.solutions.hands
    mp_hands_connections = mp_hands.HAND_CONNECTIONS

    hand_landmarks_drawing_style = mp_drawing_styles.get_default_hand_landmarks_style()
    hand_connections_drawing_stype = mp_drawing_styles.get_default_hand_connections_style()

    hands = mp_hands.Hands(model_complexity=1, min_detection_confidence=0.7, min_tracking_confidence=0.6,
                           max_num_hands=4)

    # | Posture |
    mp_pose = mp.solutions.pose
    mp_pose_connections = mp_pose.POSE_CONNECTIONS

    pose_landmarks_drawing_style = mp_drawing_styles.get_default_pose_landmarks_style()

    pose = mp_pose.Pose(model_complexity=1, min_detection_confidence=0.7, min_tracking_confidence=0.7)

    # ---------------------------------------------- #
    #             Initialisation d'OpenCV            #
    # ---------------------------------------------- #

    name = vid_name
    cap = cv2.VideoCapture(name)


    # On conserve les mêmes dimensions que la vidéo en entrée. Pour définir des dimensions particulières en sortie
    # modifier ces valeurs.
    HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    # En cas de modifications des valeurs par défauts de HIGHT et WIDTH décommenter les deux lignes suivantes.
    #cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    #cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

    # Pour l'enregistrement :
    fourcc = cv2.VideoWriter_fourcc('X', 'V', 'I', 'D')
    save_name = os.path.splitext(name)[0] + "_annotated.avi"
    out = cv2.VideoWriter(save_name, fourcc, 20.0, (WIDTH, HEIGHT))

    pTime = 0

    # --------------------------------------------- #
    #               Zones des annotations           #
    # --------------------------------------------- #

    while cap.isOpened():
        success, image = cap.read()
        # Image pour afficher les résultats

        if not success:
            print('Fin de la vidéo')
            break

        # Pour augmenter les performances (on arrête de copier l'image à chaque transformation cv2, x.process)
        annotated_img = image.copy()
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        if do_hands_drawing:
            hand_results = hands.process(image)

            if hand_results.multi_hand_landmarks:
                for hand_landmarks in hand_results.multi_hand_landmarks:
                    mp_drawing.draw_landmarks(
                        annotated_img,
                        hand_landmarks,
                        mp_hands_connections,
                        hand_landmarks_drawing_style,
                        hand_connections_drawing_stype
                    )

        if do_pose_drawing:
            pose_results = pose.process(image)

            if pose_results.pose_landmarks:
                mp_drawing.draw_landmarks(
                    annotated_img,
                    pose_results.pose_landmarks,
                    mp_pose_connections,
                    landmark_drawing_spec=pose_landmarks_drawing_style)

        # Pour arrêter l'affichage appuyer sur q pendant au moins 1 seconde.
        if cv2.waitKey(1) == ord('q'):
            break

        # Pour afficher les fps de la vidéo
        cTime = time.time()
        fps = 1 / (cTime - pTime)
        pTime = cTime

        cv2.putText(annotated_img, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3, (255, 0, 0), 3)

        # Pour afficher les résultats en direct décommenter la ligne. Le flip permet d'avoir un affichage "selfie"
        cv2.imshow('Video annotee ', cv2.flip(annotated_img, 1))

        # On enregistre le résultat
        out.write(annotated_img)

    cap.release()
    # Pour l'enregistrement vidéo
    out.release()

    # Fermeture d'OpenCv
    cv2.destroyAllWindows()
















