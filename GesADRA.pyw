# -*- coding: iso-8859-15 -*-

#----------------------------------------------------------------------------------------------------#
#   Auteur          :   F4EED - Frédéric BOUCHET  - frederic.bouchet@adrasec42.org                   #
#                   :   F4DYW - Florentin BARD    - f4dyw@free.fr                                    #
#   Refonte V6.00   :   F5IXC - Laurent LE MAGUER - f5ixc@yahoo.fr                                   #
#   Refonte V6.22b  :   F4EIR - Arnaud -                                                             #
#   Nom             :   GesADRA.pyw                                                                  #
#   Version         :   V6.22 beta 3                                                                 #
#   Date            :   Avril 2021                                                                   #
#   Description     :   Module python de creation de messages ADRASEC au format texte                #
#                       Le but de ce module est de créer des fichiers en fonction des formulaires    #
#                       d'aide a la saisie. Puis a l'aide d'un logiciel                              #
#                       exterieur de les transmettre au destinataire                                 #   
#   Creation        :   Juin 2007                                                                    #
#   Refonte         :   Avril/Septembre 2009                                                         #
#   Refonte V6.22b  :   Passage en pyton 3                                                           #
#                                                                                                    #
#   Application fonctionnant correctement sous python 3.x (et antérieures) et librairie Pmw 2.x      #
#   Pour les autres versions, les auteurs ne peuvent être tenus responsables des dysfonctionnenments #
#----------------------------------------------------------------------------------------------------#

from tkinter import *

# Modules Fonctionnels de GesADRA
from BilanAmbiance import *    # Bilans d'Ambiance
from BilanSecouriste import *  # Bilans Secourites
from GestSater import *        # Gestion des Relevés SATER
from GestPoints import *       # Gestion des Points Particuliers
from GestVictimes import *     # Gestion des Victimes
from GestMessages import *     # Gestion des messages
from MainCourante import *     # Main Courante
from MsgBT import *            # Messages Bilan Temporaire
from MsgDM import *            # Messages Demande de Moyen
from MsgOBNT import *          # Messages OBNT
from MsgIARU import *          # Messages IARU
from MsgRMD import *           # Messages RMD
from MsgTMD import *           # Messages TMD
from MsgSater import *         # Messages SATER
from MsgPOI import *           # Messages Point Particulier

import datetime
import time
import os
import tkinter.messagebox as tkMessageBox
import tkinter.filedialog as tkFileDialog
import Pmw
import sys

# Modules Techniques de GesADRA
import Commun                  # Fonctions Communes
import Session                 # Classes et fonctions relatives à la session
import Reseau                  # Fonctions de paramétrage du réseau
import Help                    # Fonctions d'aide


# Classe définissant la fenêtre principale de l'application
class MenuAdra(Tk):

    # Attributs de la classe
    cfgListe = {}
    userData = {}
    netData  = {}
    fontFixe = None
    fenMCI   = None # Référence unique sur la fenêtre Main Courante 
    fenRezo  = None # Référence unique sur la fenêtre Main Courante 
    fenGSat  = None # Référence unique sur le fenêtre Gestion des Relevés Sater
    fenGPoi  = None # Référence unique sur le fenêtre Gestion des Points Particuliers
    fenGVict = None # Référence unique sur le fenêtre Gestion des Victimes
    fenGMsg  = None # Référence unique sur le fenêtre Gestion des Messages
        
    ### Creation fenêtre principale ###
    def __init__(self):
        """Constructeur de la fenêtre principale"""

        self.root = self
        # Initialisation des dictionnaires
        self.initCfgListe("GesADRA.cfg")   # Dico de listes pour les combo-boxes
        self.initUserData(open("GesADRA.ini", 'r'))   # Dico des données utilisateur
        self.initNetData("GesADRA.net")    # Dico des données réseau

        # Construction de la fenêtre Principale
        Tk.__init__(self)
        self.geometry(("%dx%d+%d+%d")%(1024,550,0,0))
        self.resizable(width=False, height=False)

		# Mise en forme de la fenêtre
        if ( sys.platform.startswith('win')): 
            self.iconbitmap("appli.ico")
                
        self.title (self.userData['LOGICIEL'] + "-" + self.userData['VERSION'])
        self.protocol("WM_DELETE_WINDOW", self.quitterAppli)

        # Instanciation d'une bulle d'aide
        self.bulle = Pmw.Balloon(self, relmouse = 'both')
        
        # Composants de la fenêtre
        self.drawMenu()
        self.drawOthers()

        # Police fixe pour affichage des listes
        self.fonteFixe = tkFont.Font(self)
        self.fonteFixe.config(size=9, family='courier')

        # Initialisations
        self.update()
        self.timer()
        # Config.initSession(self)

        
    def drawMenu(self):

        # variables locales
        self.mainMenu = Menu()
        
        # Composants du menu

        fileMenu = Menu(self.mainMenu, tearoff=0)
        fileMenu.add_command(label="Nouveau", underline = 0, command=self.newSess)
        fileMenu.add_command(label="Ouvrir...", underline = 0, command=self.openSess)
        fileMenu.add_separator()
        self.printMenu = Menu(fileMenu, tearoff=0)
        fileMenu.add_cascade(label="Imprimer", underline = 0, menu=self.printMenu)
        fileMenu.add_separator()
        fileMenu.add_command(label="Quitter", underline = 0, command=self.quitterAppli)

        gestMenu = Menu(self.mainMenu, tearoff=0)
        gestMenu.add_command(label="Main Courante du Trafic...", underline = 5, command=self.appelMCI)
        gestMenu.add_command(label="Log. Relevés Sater...", underline = 13, command=self.appelGSat)
        gestMenu.add_command(label="Log. Points Particuliers...", underline = 5, command=self.appelGPoi)
        gestMenu.add_separator()
        gestMenu.add_command(label="Liste des Victimes...", underline = 10, command=self.appelGVict)
        gestMenu.add_command(label="Gestion des Messages...", underline = 12, command=self.appelGMsg)
        gestMenu.add_command(label="Exploitation MCI...", underline = 1, command=self.ouvrirMCI)

        msgMenu = Menu(self.mainMenu, tearoff=0)
        msgMenu.add_command(label="Standard OBNT...", command=self.appelOBNT)
        msgMenu.add_command(label="IARU Message...", command=self.appelIARU)
        msgMenu.add_command(label="Demande de Moyens...", command=self.appelMsgDM)
        msgMenu.add_command(label="Rens. Matière Dangeureuse...", command=self.appelMsgRMD)
        msgMenu.add_command(label="Transport Mat. Dangeureuse...", command=self.appelMsgTMD)
        msgMenu.add_separator()
        msgMenu.add_command(label="Bilan d'Ambiance...", command=self.appelBilAmb)
        msgMenu.add_command(label="Bilan Secouriste...", command=self.appelBilSec)
        msgMenu.add_command(label="Bilan Temporaire...", command=self.appelMsgBT)
        msgMenu.add_separator()
        msgMenu.add_command(label="Message Point Particulier...", command=self.appelMsgPOI)
        msgMenu.add_command(label="Message Relevé SATER...", command=self.appelMsgSater)

        
        cfgMenu = Menu(self.mainMenu, tearoff=0)
        cfgMenu.add_command(label="Session...", command=self.appelCfg)
        resMenu = Menu(cfgMenu, tearoff=0)
        resMenu.add_command(label="Importer...")
        cfgMenu.add_cascade(label="Réseau", menu=resMenu)

        helpMenu = Menu(self.mainMenu, tearoff=0)
        helpMenu.add_command(label="A propos...", command=self.appelAbout)

        self.mainMenu.add_cascade(label="Fichier", menu=fileMenu, underline = 0)
        self.mainMenu.add_cascade(label="Journaux", menu=gestMenu, underline = 0, state = DISABLED)
        self.mainMenu.add_cascade(label="Messages", menu=msgMenu, underline = 0, state = DISABLED)
        self.mainMenu.add_cascade(label="Paramètres", menu=cfgMenu, underline = 0, state = DISABLED)
        self.mainMenu.add_cascade(label="Aide", underline = 0, menu=helpMenu)

        self.config(menu=self.mainMenu)
        

    def drawOthers(self):

        # variables locales
        vLigne = 0
        
        # Composants de la fenêtre
        texte = "..: Aide à la gestion d'une opération de secours avec réseau d'urgence :.."
        self.tictac = StringVar()
        Label (self, text=texte, fg="blue", bg="orange").grid(row=vLigne, column=0, sticky=E+W)
        Label (self, textvariable=self.tictac, fg="blue", bg="orange", width=8).grid(row=vLigne, column=0, sticky=E)
        vLigne += 1

        self.notebook = Pmw.NoteBook(self, hull_width=1020, hull_height=510, 
                        createcommand = self.createTab, lowercommand = self.unselectTab, raisecommand = self.selectTab)
        self.notebook.grid(row = vLigne, column = 0)

    def createTab(self, page):
        """ Action à la création d'un onglet """
        
        if page == 'Gestion du Réseau':
            return
        elif page == 'Main Courante du Trafic':
            self.fenMCI.createTab()
        elif page == 'Log. Relevés Sater':
            self.fenGSat.createTab()
        elif page == 'Log. Points Particuliers':
            self.fenGPoi.createTab()
        elif page == 'Liste des Victimes':
            self.fenGVict.createTab()
            
            
    def unselectTab(self, page):
        """ Action à la désélection d'un onglet """

        if page == 'Gestion du Réseau':
            if self.fenRezo != None: self.fenRezo.unSelectTab()
        elif page == 'Main Courante du Trafic':
            if self.fenMCI != None: self.fenMCI.unSelectTab()
        elif page == 'Log. Relevés Sater':
            if self.fenGSat != None: self.fenGSat.unSelectTab()
        elif page == 'Log. Points Particuliers':
            if self.fenGPoi != None: self.fenGPoi.unSelectTab()
        elif page == 'Liste des Victimes':
            if self.fenGVict != None: self.fenGVict.unSelectTab()
                
            
    def selectTab(self, page):
        """ Action à la sélection d'un onglet """

        if page == 'Gestion du Réseau':
            if self.fenRezo != None: self.fenRezo.selectTab()
        elif page == 'Main Courante du Trafic':
            if self.fenMCI != None: self.fenMCI.selectTab()
        elif page == 'Log. Relevés Sater':
            if self.fenGSat != None: self.fenGSat.selectTab()
        elif page == 'Log. Points Particuliers':
            if self.fenGPoi != None: self.fenGPoi.selectTab()
        elif page == 'Liste des Victimes':
            if self.fenGVict != None: self.fenGVict.selectTab()

            
            
    ### Quitter l'application ###
    def quitterAppli(self):
        """Traitement du bouton Quitter"""
        
        vTitre = self.userData['LOGICIEL'] + " "+self.userData['VERSION']
        vMsg = self.userData['INDICATIF'] + ", vous allez quitter "+self.userData['LOGICIEL'] + "-" + \
               self.userData['VERSION'] + "\nVeuillez confirmer la fermeture de l'application."
        etesVousSur = tkMessageBox.askquestion(vTitre, vMsg)
        if etesVousSur == "yes" :
            if self.userData['SESSION'].strip() != "":
                Session.writeSession(self)
                Reseau.writeReseau(self)
            self.destroy()
        else:
            self.focus_set()

    ### Fonction privée Timer ###
    def timer(self):
        self.tictac.set(time.strftime('%H:%M:%S'))
        self.after(1000, self.timer)

    ### Fonction privée d'appel de la fenêtre Config ###
    def newSess(self):
        vOldSess = self.userData['SESSION'].strip()
        # Sauvegarde de l'ancienne session
        if vOldSess != "":
            Session.writeSession(self)
            Reseau.writeReseau(self)
        # Nouvelle session
        Session.FormNewSess(self)
        # Si renseignée, rafraîchissement de l'affichage
        if self.userData['SESSION'].strip() != "":
            for name in self.notebook.pagenames(): self.notebook.delete(name)
            self.fenRezo  = None
            self.fenMCI   = None
            self.fenGSat  = None
            self.fenGPoi  = None
            self.fenGVict = None
            self.fenGMsg  = None        
            self.mainMenu.entryconfigure("Journaux", state = NORMAL)
            self.mainMenu.entryconfigure("Messages", state = NORMAL)
            self.mainMenu.entryconfigure("Paramètres", state = NORMAL)
            self.appelRes()

    def openSess(self):
        vOldSess = self.userData['SESSION'].strip()
        # Sauvegarde de l'ancienne session
        if vOldSess != "":
            Session.writeSession(self)
            Reseau.writeReseau(self)
        # Ouverture d'une session
        Session.openSess(self)
        # Si différente, rafraîchissement de l'affichage
        if self.userData['SESSION'].strip() != vOldSess:
            for name in self.notebook.pagenames(): self.notebook.delete(name)
            self.fenRezo  = None
            self.fenMCI   = None
            self.fenGSat  = None
            self.fenGPoi  = None
            self.fenGVict = None
            self.fenGMsg  = None        
            self.mainMenu.entryconfigure("Journaux", state = NORMAL)
            self.mainMenu.entryconfigure("Messages", state = NORMAL)
            self.mainMenu.entryconfigure("Paramètres", state = NORMAL)
            self.appelRes()
            
            
    ### Fonction privée d'appel de la fenêtre Config ###
    def appelCfg(self):
        Session.FormSession(self)


    ### Fonction privée d'appel de la fenêtre Réseau ###
    def appelRes(self):
        if self.fenRezo == None:
            self.fenRezo = Reseau.FormReseau(self)
        else:
            self.notebook.selectpage('Gestion du Réseau')

    ### Fonction privée d'appel de la fenêtre Aide ###
    def appelAbout(self):
        Help.FormAbout(self)

    ### Fonction privée d'appel de la fenêtre MCI ###
    def appelMCI(self):
        # Appel de la fenêtre Main Courante avec contrôle de son unicité 
        if self.fenMCI == None :
            self.fenMCI = FormMCI(self)
        self.notebook.selectpage('Main Courante du Trafic')

    ### Fonction privée d'appel de la fenêtre GSAT ###
    def appelGSat(self):
        # Appel de la fenêtre Gestion Sater avec contrôle de son unicité 
        if self.fenGSat == None :
            self.fenGSat = FormGSat(self)
        self.notebook.selectpage('Log. Relevés Sater')

    ### Fonction privée d'appel de la fenêtre GPOI ###
    def appelGPoi(self):
        # Appel de la fenêtre Gestion POI avec contrôle de son unicité 
        if self.fenGPoi == None :
            self.fenGPoi = FormGPoi(self)
        self.notebook.selectpage('Log. Points Particuliers')

    ### Fonction privée d'appel de la fenêtre GVict ###
    def appelGVict(self):
        # Appel de la fenêtre Gestion des Victimes avec contrôle de son unicité 
        if self.fenGVict == None :
            self.fenGVict = FormGVict(self)
        self.notebook.selectpage('Liste des Victimes')

    ### Fonction privée d'appel de la fenêtre Gestion des Messages ###
    def appelGMsg(self):

        tkMessageBox.showinfo("Gestion des Messages", \
                              "Fonctionnalité en cours de développement")
        return False

        # Appel de la fenêtre Main Courante avec contrôle de son unicité 
        if self.fenGMsg == None :
            self.fenGMsg = FormGMsg(self, onglet)
        else :
            self.fenGMsg.fenetre.focus_set()

    ### Fonction privée d'appel de la fenêtre MCI ###
    def ouvrirMCI(self):
        tkMessageBox.showinfo("Gestion des Messages", \
                              "Fonctionnalité en cours de développement")
        return False

    ### Fonction privée d'appel de la fenêtre OBNT ###
    def appelOBNT(self):
        FormOBNT(self)

    ### Fonction privée d'appel de la fenêtre IARU ###
    def appelIARU(self):
        FormIARU(self)

    ### Fonction privée d'appel de la fenêtre BT ###
    def appelMsgBT(self):
        FormBT(self)

    ### Fonction privée d'appel de la fenêtre DM ###
    def appelMsgDM(self):
        FormDM(self)

    ### Fonction privée d'appel de la fenêtre RMD ###
    def appelMsgRMD(self):
        FormRMD(self)

    ### Fonction privée d'appel de la fenêtre TMD ###
    def appelMsgTMD(self):
        FormTMD(self)

    ### Fonction privée d'appel de la fenêtre Bilan Secouriste ###
    def appelBilSec(self):
        FormBILSEC(self)

    ### Fonction privée d'appel de la fenêtre Bilan Ambiance ###
    def appelBilAmb(self):
        FormBilAmb(self)

    ### Fonction privée d'appel de la fenêtre POI ###
    def appelMsgPOI(self):
        FormPOI(self)

    ### Fonction privée d'appel de la fenêtre Sater ###
    def appelMsgSater(self):
        FormSATER(self)

    ### Fichier de Configuration ###
    def initCfgListe(self, ficCfg):
        "Alimente le dictionnaire de configuration avec des listes de valeurs"
        # Ouverture du fichier de configuration en mode lecture
        fic = open(ficCfg,'r', encoding='iso-8859-15') 
        lignes = fic.readlines() ## Récupération du contenu du fichier
        fic.close()
        for lig in lignes:
            sp = lig.split('#')[0] # Elimination des commentaires potentiels
            sp = lig.split('[')[0] # Elimination des sections
            sp = sp.split('=')     # Séparation variable sur le signe '=' valeur
            # on teste la longueur de sp;  si elle n'est pas égale à 2, c'est qu'il s'agit d'une ligne vide ou qu'avec des commentaires
            if len(sp) == 2:
                cle   = sp[0].strip()
                liste = sp[1].strip().split(',')
                self.cfgListe[cle] = liste
        
    ### Fichier de Données utilisateur ###
    def initUserData(self, ficUser):
        "Alimente le dictionnaire de configuration avec des valeurs du fichier"
        # Nettoyage du dictionnaire
        self.userData.clear()
        # Ouverture du fichier utilisateur en mode lecture
        # fic = open(ficUser,'r') 
        lignes = ficUser.readlines() # Récupération du contenu du fichier
        ficUser.close() 
        for lig in lignes:
            sp = lig.split('#')[0] # Elimination des commentaires potentiels
            sp = lig.split('[')[0] # Elimination des sections
            sp = sp.split('=')     # Séparation  des variables sur le signe '='
            # on teste la longueur de sp;  si elle n'est pas égale à 2, c'est qu'il s'agit d'une ligne vide ou qu'avec des commentaires
            if len(sp) == 2:
                cle    = sp[0].strip()
                valeur = sp[1].strip()
                self.userData[cle] = valeur

    ### Fichier de Données réseau ###
    def initNetData(self, ficNet):
        "Alimente le dictionnaire des stations du réseau avec des valeurs du fichier"
        # Nettoyage du dictionnaire
        self.netData.clear()
        # Ouverture du fichier utilisateur en mode lecture
        fic = open(ficNet,'r') 
        lignes = fic.readlines() # Récupération du contenu du fichier
        fic.close() 
        for lig in lignes:
            sp = lig.split('#')[0] # Elimination des commentaires potentiels
            sp = lig.split('[')[0] # Elimination des sections
            sp = sp.split('=')     # Séparation  des variables sur le signe '='
            # on teste la longueur de sp;  si elle n'est pas égale à 2, c'est qu'il s'agit d'une ligne vide ou qu'avec des commentaires
            if len(sp) == 2:
                cle    = sp[0].strip()
                valeur = sp[1].strip()
                self.netData[cle] = valeur



################################
#  Lancement de l'application  #
#                              #
if __name__ == '__main__':
    gesADRA = MenuAdra()
    gesADRA.mainloop()
    exit
#                              #
################################
