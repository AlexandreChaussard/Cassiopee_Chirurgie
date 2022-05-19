import cv2

video_name = 'LEJAY/LEJAY_p2_short.mp4'

"""
Ce programme comporte des fonctions permettant de :
- Afficher une vidéo enregistrée sur l'ordi
- Convertir une video au format .avi en vidéo au format .mp4 et de changer les fps si besoin
- Prendre des photos à partir de la vidéo obtenue par la caméra

À terme :
- Transformer une vidéo en d'images (presque tout fait à image, suc = cap.read() d'openCV)
"""


def avi_to_mp4(video_name, save_bool):
    cap = cv2.VideoCapture(video_name)

    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

    i = 0
    nb_saves_images = 0
    seuil_nb_image = 350
    saved_video_name = 'output.mp4'
    saved_video_fps = 15

    if save_bool:
        fourcc = cv2.VideoWriter_fourcc('m', 'p', '4', 'v')
        out = cv2.VideoWriter(saved_video_name, fourcc, saved_video_fps, (width, height))

    while True:
        ret, frame = cap.read()

        if not ret:
            print('Flux non trouvé')
            break

        # Pour savoir à quelle image nous sommes
        if not i % 100:
            print("Image n° " + str(i))

        frame = cv2.flip(frame, 1)
        cv2.imshow('Frame', frame)

        # save_bool = True si on souhaite enregistrer les images qui s'affichent
        if save_bool:
            out.write(frame)

        if cv2.waitKey(1) == ord('s'):
            nb_saves_images += 1
            cv2.imwrite('image_' + str(nb_saves_images) + '.jpg', frame)

        if cv2.waitKey(1) == ord('q'):
            break

        if i > seuil_nb_image:  # Pour arrêter la video à seuil_nb_images images
            break

        i += 1

    cap.release()
    out.release()
    cv2.destroyAllWindows()


def images_from_camera():
    cap = cv2.VideoCapture(0)
    nb_photos_taken = 1

    while True:
        ret, frame = cap.read()
        print('Here ' + str(nb_photos_taken))

        if not ret:
            print('Caméra Non Trouvée')
            break

        cv2.imshow('Frame', frame)

        if cv2.waitKey(1) == ord("s"):
            cv2.imwrite(str(nb_photos_taken) + '.jpg', frame)
            nb_photos_taken += 1

        if cv2.waitKey(1) == ord("q"):
            break

    cap.release()
    cv2.destroyAllWindows()


def display_video(video_name):
    avi_to_mp4(video_name, False)


#display_video(video_name)
#images_from_camera()
avi_to_mp4("AUBERTIN_Passage1_film_RGB.avi", True)  # video_name = 0 permet d'accéder à la caméra