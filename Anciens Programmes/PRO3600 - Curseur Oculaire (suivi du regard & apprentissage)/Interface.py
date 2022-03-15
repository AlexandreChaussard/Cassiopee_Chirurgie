from tkinter import *
from RoundButton import *

"""
Interface permet l'affichage de la partie controle final du curseur par l'oeil
"""


# Affiche les boutons utilisateurs (exit & étalonnage)
def displayButtons(cs):
    """ Affiche les boutons utilisateurs (exit & étalonnage)

    :param cs: instance d'un objet CursorScaling
    :return: None
    """
    # Appel d'une fenêtre tk
    cs.fenetre = Tk()
    # Mode fullscreen
    cs.fenetre.attributes('-fullscreen', True)
    # Echap permet de quitter l'interface
    cs.fenetre.bind('<Escape>', lambda e: cs.fenetre.destroy())
    # Récupération des informations de l'écran
    width = cs.fenetre.winfo_screenwidth()
    height = cs.fenetre.winfo_screenheight()
    # initialisation des positions des boutons étalons
    etan = Button(cs.fenetre, text='étalonnage', command=cs.launchCalibrating,
                  background="#494949", foreground="#F90808",
                  relief=GROOVE, height=2, width=9, bd=4.55, font="serif", activebackground="#6B6B6B")
    etan.place(x=100, y=100)
    etan.grid()
    quitButton = tk.Button(cs.fenetre, text='quitter', command=cs.quitProcess,
                           background="#494949", foreground="#F90808",
                           relief=GROOVE, height=2, width=9, bd=4.55, font="serif", activebackground="#6B6B6B")
    quitButton.place(x=600, y=100)
    quitButton.grid()

    # création de la fenêtre
    canvas = tk.Canvas(cs.fenetre, width=width, height=height, bg='black')
    canvas.grid()
    cs.fenetre.mainloop()
    return
