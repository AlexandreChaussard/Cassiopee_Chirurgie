import mediapipe as mp
import cv2

from programmes_annexes import get_label

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands


def drawing_hands(hand_results, image):

    HEIGHT = len(image)
    WIDTH = len(image[0])

    for num, hand_landmarks in enumerate(hand_results.multi_hand_landmarks):
        mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            mp_hands.HAND_CONNECTIONS,
            mp_drawing_styles.get_default_hand_landmarks_style(),
            mp_drawing_styles.get_default_hand_connections_style())

        if get_label(mp_hands, hand_landmarks, num, hand_results, HEIGHT, WIDTH, False):
            text, coords = get_label(mp_hands, hand_landmarks, num, hand_results, HEIGHT, WIDTH, False)
            cv2.putText(image, text, coords, cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), thickness=2, lineType=cv2.LINE_AA)

    return image
