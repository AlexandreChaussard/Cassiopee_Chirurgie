import tkinter as tk

"""
Class définissant des boutons ronds | Récupération retravaillée de la source :
https://stackoverflow.com/questions/42579927/rounded-button-tkinter-python/45536589
"""


class RoundButton(tk.Canvas):

    def __init__(self, parent, width, height, cornerradius, padding, color, bg, scaler):
        """ Constructeur de RoundButton

        :param parent: canvas parent tkinter
        :param width: largeur du bouton
        :param height: hauteur du bouton
        :param cornerradius: rayon du cercle
        :param padding: remplissage
        :param color: couleur
        :param bg: fond
        :param scaler: instance d'un objet CursorScaling
        """
        tk.Canvas.__init__(self, parent, borderwidth=0,
                           relief="flat", highlightthickness=0, bg=bg)

        # Le bouton doit pouvoir disparaître dans le scaler, on a donc besoin de l'instance
        self.scaler = scaler

        if cornerradius > 0.5 * width:
            print("Error: cornerradius is greater than width.")
            return None

        if cornerradius > 0.5 * height:
            print("Error: cornerradius is greater than height.")
            return None

        rad = 2 * cornerradius

        def shape():
            self.create_polygon((padding, height - cornerradius - padding, padding, cornerradius + padding,
                                 padding + cornerradius, padding, width - padding - cornerradius, padding,
                                 width - padding, cornerradius + padding, width - padding,
                                 height - cornerradius - padding, width - padding - cornerradius, height - padding,
                                 padding + cornerradius, height - padding), fill=color, outline=color)
            self.create_arc((padding, padding + rad, padding + rad, padding), start=90, extent=90, fill=color,
                            outline=color)
            self.create_arc((width - padding - rad, padding, width - padding, padding + rad), start=0, extent=90,
                            fill=color, outline=color)
            self.create_arc((width - padding, height - rad - padding, width - padding - rad, height - padding),
                            start=270, extent=90, fill=color, outline=color)
            self.create_arc((padding, height - padding - rad, padding + rad, height - padding), start=180, extent=90,
                            fill=color, outline=color)

        id = shape()
        (x0, y0, x1, y1) = self.bbox("all")
        width = (x1 - x0)
        height = (y1 - y0)
        self.configure(width=width, height=height)
        self.bind("<ButtonPress-1>", self._on_press)
        self.bind("<ButtonRelease-1>", self._on_release)

    def _on_press(self, event):
        """ Action effectuée quand évènement de clic sur le bouton

        :param event: Evenement de clic
        :return: None
        """
        self.configure(relief="sunken")
        if self.scaler is not None:
            self.scaler.pointClickEvent(self)

    def _on_release(self, event):
        """ Action effectuée quand relachement du bouton

        :param event: Evenement de relachement
        :return: None
        """
        self.configure(relief="raised")
