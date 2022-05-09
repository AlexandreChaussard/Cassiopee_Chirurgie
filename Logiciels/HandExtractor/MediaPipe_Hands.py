import cv2
import mediapipe as mp
from Video import VideoObject

from hands_drawing_mp import drawing_hands

DEBUG = True

class HandTracker:

    def __init__(self, path):
        # Pour les mains :
        self.path = path
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(model_complexity=1, min_detection_confidence=0.6, min_tracking_confidence=0.5,
                                         max_num_hands=2)

        # Pour la position :
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(model_complexity=1, min_detection_confidence=0.7, min_tracking_confidence=0.6)

        self.video = VideoObject(path)

    def launch(self):

        file = open(self.path + "_handstracking.txt", 'w')
        frameCount = 0

        handsDenomination = ["None", "None"]
        while self.video.video.isOpened():
            frameCount += 1
            success, image = self.video.getNextView()

            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                # continue
                break

            # Les fonctions arrêtent de copier l'image à chaque transformation (augmente les performances)
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # On créé une nouvelle image sur laquelle on va afficher les annotations.
            annotated_img = image.copy()
            annotated_img = cv2.cvtColor(annotated_img, cv2.COLOR_RGB2BGR)

            # Détection des mains :
            hand_results = self.hands.process(annotated_img)

            if hand_results.multi_hand_landmarks:
                if DEBUG:
                    drawing_hands(hand_results, annotated_img)

                for idx, hand_handedness in enumerate(hand_results.multi_handedness):
                    for index, classif in enumerate(hand_handedness.classification):
                        if classif.label == "Right":
                            handsDenomination[1] = classif.label
                        else:
                            handsDenomination[0] = classif.label

                for num, hand_landmarks in enumerate(hand_results.multi_hand_landmarks):
                    if num >= len(handsDenomination):
                        continue
                    handLabel = handsDenomination[num]
                    line = str(self.video.getCurrentFrameIndex()) + ";" + handLabel + ":"
                    for idx, landmark in enumerate(hand_landmarks.landmark):
                        line = line + str(idx) + ";" + str(landmark.x) + ";" + str(landmark.y) + ";" + str(landmark.z) + "|"
                    line = line[0:len(line)-2] + "\n"
                    file.write(line)

            if DEBUG:
                # Flip the image horizontally for a selfie-view display.
                cv2.imshow('MediaPipe Hands', cv2.flip(annotated_img, 1))

            if cv2.waitKey(5) & 0xFF == 27:
                break

        file.close()
        self.video.video.release()
        cv2.destroyAllWindows()
