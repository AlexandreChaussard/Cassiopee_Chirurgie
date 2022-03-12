import cv2


class VideoObject:

    def __init__(self, video_path):
        self.currentView = None
        self.image_index = 0
        self.video = cv2.VideoCapture(video_path)
        if not self.video.isOpened():
            raise ValueError("Unable to open video source", video_path)

        # Get video source width and height
        self.width = self.video.get(cv2.CAP_PROP_FRAME_WIDTH)
        self.height = self.video.get(cv2.CAP_PROP_FRAME_HEIGHT)
        self.frame_count = self.video.get(cv2.CAP_PROP_FRAME_COUNT)

    # Release the video source when the object is destroyed
    def __del__(self):
        if self.video.isOpened():
            self.video.release()

    # Renvoie une image cv2 de la vidéo spécifié
    def getNextView(self):
        """ Récupère l'image courante de la vidéo
        """
        ret = None
        if self.video.isOpened():

            ret, frame = self.video.read()
            self.currentView = [ret, frame]

            if ret:
                # Return a boolean success flag and the current frame converted to BGR
                return (ret, cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))
            else:
                return (ret, None)
        else:
            return (ret, None)

    # Renvoie une image cv2 de la vidéo spécifié
    def getCurrentView(self):
        if self.currentView is not None:
            return (self.currentView[0], cv2.cvtColor(self.currentView[1], cv2.COLOR_BGR2RGB))
        else:
            return None
