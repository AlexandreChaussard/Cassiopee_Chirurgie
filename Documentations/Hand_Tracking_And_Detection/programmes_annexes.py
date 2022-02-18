import numpy as np


def get_label(mp_hands, hand, index, results, lenght, width, with_world):
    output = None
    for idx, classification in enumerate(results.multi_handedness):

        # Classification.classification est de la forme {label, score, index}
        print(len(results.multi_handedness))

        if classification.classification[0].index == (index + (len(results.multi_handedness) == 1)*classification.classification[0].index):
            label = classification.classification[0].label[0]
            score = round(classification.classification[0].score, 2)
            text = '{} {}'.format(label, score)

            # On place le texte au bon endroit (selon l'option choisie pour mediapipe, hand_landmarks_world -> Coord non normalisées)
            if not with_world:
                coords = tuple(np.multiply(
                    [hand.landmark[mp_hands.HandLandmark.WRIST].x, hand.landmark[mp_hands.HandLandmark.WRIST].y],
                    [lenght, width]
                ).astype(int))

            else:
                coords = tuple(np.array(
                    [hand.landmark[mp_hands.HandLandmark.WRIST].x, hand.landmark[mp_hands.HandLandmark.WRIST].y]
                ))

            output = text, coords

    return output


def get_wrist_pos(hand, results):
    output = None
    for idx, test in enumerate(hand):
        pass

    return output




