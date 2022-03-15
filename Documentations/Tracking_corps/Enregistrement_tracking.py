import cv2
import mediapipe as mp
import time
import os
from os import listdir
from os.path import splitext, exists

from programmes_annexes import get_label

# Trouver le path des fichiers
path = os.getcwd()
input_file_path = f"{path}\\Input_Files_Avi"
# Liste les fichiers .avi dans la direction Input_Files_Avi
if not exists(input_file_path):
    raise Exception(f"No such folder {input_file_path}")

files = [f for f in listdir(input_file_path) if splitext(f)[1] == ".avi"]

# Automatic treatment for all files
for i in range(len(files)):
    filename = files[i]
    print(filename)
    mp_drawing = mp.solutions.drawing_utils
    mp_drawing_styles = mp.solutions.drawing_styles
    mp_hands = mp.solutions.hands
    mpDraw = mp.solutions.drawing_utils
    mpPose = mp.solutions.pose
    pose = mpPose.Pose()
    print(mp_drawing)
    print(mpDraw)

    cap = cv2.VideoCapture(path+"\\Input_Files_Avi\\"+filename)
    pTime = 0
    # Modifier la taille de l'affichage vidéo :
    HEIGHT = 1500
    WIDTH = 1500

    cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

    fw = int(cap.get(3))
    fh = int(cap.get(4))
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter(path+"\\Output_Files_Avi\\"+filename[:-4]+"_tracking.avi", fourcc, 20.0, (fw,  fh))

    nb_frame=0
    print("Ok ok")
    with mp_hands.Hands(
        model_complexity=1,
        min_detection_confidence=0.5,
        min_tracking_confidence=0.5,
        max_num_hands=4) as hands:


        while cap.isOpened():
            success, image = cap.read()

            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                break

            # if nb_frame>300:
            #     break
            print("détection ok")
            # Détection :
            # Les fonctions arrêtent de copier l'image à chaque transformation (augmente les performances)
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = hands.process(image)
            results2 = pose.process(image)


            # Draw the hand annotations on the image.
            image.flags.writeable = True
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)


            if results2.pose_landmarks:
                mpDraw.draw_landmarks(image, results2.pose_landmarks, mpPose.POSE_CONNECTIONS)
                for id, lm in enumerate(results2.pose_landmarks.landmark):
                    h, w, c = image.shape
                    #print(id, lm)
                    cx, cy = int(lm.x * w), int(lm.y * h)
                    cv2.circle(image, (cx, cy), 5, (255, 0, 0), cv2.FILLED)

                cTime = time.time()
                fps = 1 / (cTime - pTime)
                pTime = cTime

                cv2.putText(image, str(int(fps)), (70, 50), cv2.FONT_HERSHEY_PLAIN, 3,
                    (255, 0, 0), 3)


            if results.multi_hand_landmarks:
                for num, hand_landmarks in enumerate(results.multi_hand_landmarks):
                    mp_drawing.draw_landmarks(
                        image,
                        hand_landmarks,
                        mp_hands.HAND_CONNECTIONS,
                        mp_drawing_styles.get_default_hand_landmarks_style(),
                        mp_drawing_styles.get_default_hand_connections_style())

                    if get_label(mp_hands, hand_landmarks, num, results, HEIGHT, WIDTH, False):
                        text, coords = get_label(mp_hands, hand_landmarks, num, results, HEIGHT, WIDTH, False)
                        cv2.putText(image, text, coords, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), thickness=2, lineType=cv2.LINE_AA)
            # Flip the image horizontally for a selfie-view display.
            cv2.imshow('MediaPipe Hands', cv2.flip(image, 1))
            out.write(image)
            nb_frame+=1

            if cv2.waitKey(1) == ord('q'):
                break

    cap.release()
    
    out.release()
    cv2.destroyAllWindows()