# -*- coding: iso-8859-15 -*-

from tkinter import *

import Pmw

class FormAbout(Toplevel):
    """Classe d�finissant la fen�tre Aide"""
    
    def __init__(self, appli):
        """Constructeur de la fen�tre Aide"""

        # Nouvelle fen�tre pour Pmw
        Toplevel.__init__(self)
        Pmw.initialise()
        # Param�trage de la fen�tre
        self.iconbitmap("appli.ico")
        self.resizable(width = False, height = False)
        self.wm_state()
        self.title ("Aide")
        # C'est une fen�tre modale
        self.transient(appli)
        self.grab_set() 
        self.focus_set()

        # Composants de la fen�tre
        self.soft = StringVar()
        Label (self, textvariable = self.soft, font=appli.fonteFixe).grid(row=1, column=0, sticky=W+E)
        Label (self, text = "Aide � la gestion d'une op�ration", fg="blue", bg="orange").grid(row = 2, column = 0, sticky = W+E)
        Label (self, text = "de secours avec r�seau d'urgence.", fg="blue", bg="orange").grid(row = 3, column = 0, sticky = W+E)
        self.web = StringVar()
        Label (self, textvariable = self.web, font=appli.fonteFixe).grid(row=4, column=0, sticky=W+E)
		
        Button(self, text = "OK", width = 10, command = self.destroy, fg = "blue").grid (row = 5, column = 0)
        
        # Initialisation
        self.soft.set(appli.userData['LOGICIEL'] + " " + appli.userData['VERSION'])
        self.web.set("www.gesadra.fr")

#
#
