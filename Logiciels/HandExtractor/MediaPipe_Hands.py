import cv2
import mediapipe as mp
from Video import VideoObject


class HandTracker:

    def __init__(self, path):
        # Pour les mains :
        self.path = path
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(model_complexity=1, min_detection_confidence=0.6, min_tracking_confidence=0.5,
                                         max_num_hands=4)

        # Pour la position :
        self.mpPose = mp.solutions.pose
        self.pose = self.mpPose.Pose(model_complexity=1, min_detection_confidence=0.7, min_tracking_confidence=0.6)

        self.video = VideoObject(path)

    def launch(self):

        file = open(self.path + "_handstracking.txt", 'w')
        while self.video.video.isOpened():
            success, image = self.video.getNextView()

            if not success:
                print("Ignoring empty camera frame.")
                # If loading a video, use 'break' instead of 'continue'.
                # continue
                break

            # Les fonctions arrêtent de copier l'image à chaque transformation (augmente les performances)
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

            # Détection des mains :
            hand_results = self.hands.process(image)

            if hand_results.multi_hand_landmarks:
                for num, hand_landmarks in enumerate(hand_results.multi_hand_landmarks):
                    line = str(self.video.getCurrentFrameIndex()) + ":"
                    for idx, landmark in enumerate(hand_landmarks.landmark):
                        line = line + str(idx) + ";" + str(landmark.x) + ";" + str(landmark.y) + ";" + str(landmark.z) + "|"
                    line = line[0:len(line)-2] + "\n"
                file.write(line)

            if cv2.waitKey(5) & 0xFF == 27:
                break

        file.close()
        self.video.video.release()
        cv2.destroyAllWindows()
