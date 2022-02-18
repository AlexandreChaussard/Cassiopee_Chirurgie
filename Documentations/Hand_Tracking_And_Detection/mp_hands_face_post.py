import cv2
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_holistic = mp.solutions.holistic

name = 'CHAKFE/chakfe_short_no_anno.mp4'
cap = cv2.VideoCapture(0)

with mp_holistic.Holistic(
    model_complexity=2,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.6,
    enable_segmentation=True,
    refine_face_landmarks=True,
    ) as holistic:

  while cap.isOpened():
    success, image = cap.read()
    if not success:
      print("Ignoring empty camera frame.")
      # If loading a video, use 'break' instead of 'continue'.
      #continue
      break

    # To improve performance, optionally mark the image as not writeable to
    # pass by reference.
    image.flags.writeable = False
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    results = holistic.process(image)

    # Draw landmark annotation on the image.
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    mp_drawing.draw_landmarks(
        image,
        results.face_landmarks,
        mp_holistic.FACEMESH_CONTOURS,
        landmark_drawing_spec=None,
        connection_drawing_spec=mp_drawing_styles
        .get_default_face_mesh_contours_style())

    #mp_drawing.draw_landmarks(
    #    image=image,
    #    landmark_list=results.face_landmarks,
    #    connections=mp_holistic.FACEMESH_TESSELATION,
    #    landmark_drawing_spec=None,
    #    connection_drawing_spec=mp_drawing_styles
    #        .get_default_face_mesh_tesselation_style())

    #mp_drawing.draw_landmarks(
    #    image=image,
    #    landmark_list=results.face_landmarks,
    #    connections=mp_holistic.FACEMESH_IRISES,
    #    landmark_drawing_spec=None,
    #    connection_drawing_spec=mp_drawing_styles
    #        .get_default_face_mesh_iris_connections_style())

    #mp_drawing.draw_landmarks(
    #    image,
    #    results.pose_landmarks,
    #    mp_holistic.POSE_CONNECTIONS,
    #    landmark_drawing_spec=mp_drawing_styles
    #    .get_default_pose_landmarks_style())

    mp_drawing.draw_landmarks(
        image,
        results.left_hand_landmarks,
        mp_holistic.HAND_CONNECTIONS,
        mp_drawing_styles.get_default_hand_landmarks_style(),
        mp_drawing_styles.get_default_hand_connections_style()
    )

    mp_drawing.draw_landmarks(
        image,
        results.right_hand_landmarks,
        mp_holistic.HAND_CONNECTIONS,
        mp_drawing_styles.get_default_hand_landmarks_style(),
        mp_drawing_styles.get_default_hand_connections_style()
    )

    # Flip the image horizontally for a selfie-view display.
    cv2.imshow('MediaPipe Holistic', cv2.flip(image, 1))

    if cv2.waitKey(1) & 0xFF == 27:
      break

cap.release()
cv2.destroyAllWindows()