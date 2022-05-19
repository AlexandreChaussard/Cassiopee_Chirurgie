import cv2
import mediapipe as mp


from hands_drawing_mp import drawing_hands


# Pour les mains :
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(model_complexity=1, min_detection_confidence=0.6, min_tracking_confidence=0.5, max_num_hands=4)

# Pour la position :
mpPose = mp.solutions.pose
pose = mpPose.Pose(model_complexity=1, min_detection_confidence=0.7, min_tracking_confidence=0.6)

name = 'LEJAY/LEJAY_p2_short.mp4'
cap = cv2.VideoCapture('LEJAY/LEJAY_p2_short.mp4')

# ----- Modifier la taille de l'affichage vidéo : ------

HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

#cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
#cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

# ------------

# Pour l'enregistrement vidéo
fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
out = cv2.VideoWriter('test_lejay.mp4', fourcc, 15, (WIDTH,  HEIGHT)) #15 correspond au fps


while cap.isOpened():
    success, image = cap.read()

    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      #continue
      break

    # Les fonctions arrêtent de copier l'image à chaque transformation (augmente les performances)
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Détection des mains :
    hand_results = hands.process(image)

    # Détection de la posture
    pose_results = pose.process(image)

    # On créé une nouvelle image sur laquelle on va afficher les annotations.
    annotated_img = image.copy()
    annotated_img = cv2.cvtColor(annotated_img, cv2.COLOR_RGB2BGR)

    if hand_results.multi_hand_landmarks:
        drawing_hands(hand_results, annotated_img)

    # Flip the image horizontally for a selfie-view display.
    out.write(cv2.flip(annotated_img, 1))
    cv2.imshow('MediaPipe Hands', cv2.flip(annotated_img, 1))

    if cv2.waitKey(5) & 0xFF == 27:
      break

cap.release()

# Pour l'enregistrement vidéo
out.release()
cv2.destroyAllWindows()