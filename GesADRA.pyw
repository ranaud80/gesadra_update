# -*- coding: iso-8859-15 -*-

#----------------------------------------------------------------------------------------------------#
#   Auteur          :   F4EED - Fr�d�ric BOUCHET  - frederic.bouchet@adrasec42.org                   #
#                   :   F4DYW - Florentin BARD    - f4dyw@free.fr                                    #
#   Refonte V6.00   :   F5IXC - Laurent LE MAGUER - f5ixc@yahoo.fr                                   #
#   Nom             :   GesADRA.pyw                                                                  #
#   Version         :   V6.21                                                                        #
#   Date            :   Mai 2011                                                             #
#   Description     :   Module python de creation de messages ADRASEC au format texte                #
#                       Le but de ce module est de cr�er des fichiers en fonction des formulaires    #
#                       d'aide a la saisie. Puis a l'aide d'un logiciel                              #
#                       exterieur de les transmettre au destinataire                                 #   
#   Creation        :   Juin 2007                                                                    #
#   Refonte         :   Avril/Septembre 2009                                                         #
#                                                                                                    #
#   Application fonctionnant correctement sous python 2.6 (et ant�rieures) et librairie Pmw 1.3.2    #
#   Pour les autres versions, les auteurs ne peuvent �tre tenus responsables des dysfonctionnenments #
#----------------------------------------------------------------------------------------------------#

from Tkinter import *

# Modules Fonctionnels de GesADRA
from BilanAmbiance import *    # Bilans d'Ambiance
from BilanSecouriste import *  # Bilans Secourites
from GestSater import *        # Gestion des Relev�s SATER
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
import tkMessageBox
import tkFileDialog
import Pmw
import sys

# Modules Techniques de GesADRA
import Commun                  # Fonctions Communes
import Session                 # Classes et fonctions relatives � la session
import Reseau                  # Fonctions de param�trage du r�seau
import Help                    # Fonctions d'aide


# Classe d�finissant la fen�tre principale de l'application
class MenuAdra(Tk):

    # Attributs de la classe
    cfgListe = {}
    userData = {}
    netData  = {}
    fontFixe = None
    fenMCI   = None # R�f�rence unique sur la fen�tre Main Courante 
    fenRezo  = None # R�f�rence unique sur la fen�tre Main Courante 
    fenGSat  = None # R�f�rence unique sur le fen�tre Gestion des Relev�s Sater
    fenGPoi  = None # R�f�rence unique sur le fen�tre Gestion des Points Particuliers
    fenGVict = None # R�f�rence unique sur le fen�tre Gestion des Victimes
    fenGMsg  = None # R�f�rence unique sur le fen�tre Gestion des Messages
        
    ### Creation fen�tre principale ###
    def __init__(self):
        """Constructeur de la fen�tre principale"""

        self.root = self
        # Initialisation des dictionnaires
        self.initCfgListe("GesADRA.cfg")   # Dico de listes pour les combo-boxes
        self.initUserData(open("GesADRA.ini", 'rb'))   # Dico des donn�es utilisateur
        self.initNetData("GesADRA.net")    # Dico des donn�es r�seau

        # Construction de la fen�tre Principale
        Tk.__init__(self)
        self.geometry(("%dx%d+%d+%d")%(1024,550,0,0))
        self.resizable(width=False, height=False)

		# Mise en forme de la fen�tre
        self.iconbitmap("appli.ico")
        self.title (self.userData['LOGICIEL'] + "-" + self.userData['VERSION'])
        self.protocol("WM_DELETE_WINDOW", self.quitterAppli)

        # Instanciation d'une bulle d'aide
        self.bulle = Pmw.Balloon(self, relmouse = 'both')
        
        # Composants de la fen�tre
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
        #gestMenu.add_command(label="Log. Relev�s Sater...", underline = 13, command=self.appelGSat)
        #gestMenu.add_command(label="Log. Points Particuliers...", underline = 5, command=self.appelGPoi)
        gestMenu.add_separator()
        gestMenu.add_command(label="Liste des Victimes...", underline = 10, command=self.appelGVict)
        #gestMenu.add_command(label="Gestion des Messages...", underline = 12, command=self.appelGMsg)
        #gestMenu.add_command(label="Exploitation MCI...", underline = 1, command=self.ouvrirMCI)

        msgMenu = Menu(self.mainMenu, tearoff=0)
        msgMenu.add_command(label="Standard OBNT...", command=self.appelOBNT)
        #msgMenu.add_command(label="IARU Message...", command=self.appelIARU)
        msgMenu.add_command(label="Demande de Moyens...", command=self.appelMsgDM)
        msgMenu.add_command(label="Rens. Mati�re Dangeureuse...", command=self.appelMsgRMD)
        msgMenu.add_command(label="Transport Mat. Dangeureuse...", command=self.appelMsgTMD)
        msgMenu.add_separator()
        msgMenu.add_command(label="Bilan d'Ambiance...", command=self.appelBilAmb)
        msgMenu.add_command(label="Bilan Secouriste...", command=self.appelBilSec)
        msgMenu.add_command(label="Bilan Temporaire...", command=self.appelMsgBT)
        msgMenu.add_separator()
        msgMenu.add_command(label="Message Point Particulier...", command=self.appelMsgPOI)
        #msgMenu.add_command(label="Message Relev� SATER...", command=self.appelMsgSater)

        
        cfgMenu = Menu(self.mainMenu, tearoff=0)
        cfgMenu.add_command(label="Session", command=self.appelCfg)
        resMenu = Menu(cfgMenu, tearoff=0)
        resMenu.add_command(label="Importer...")
        #cfgMenu.add_cascade(label="R�seau", menu=resMenu)

        helpMenu = Menu(self.mainMenu, tearoff=0)
        helpMenu.add_command(label="A propos...", command=self.appelAbout)

        self.mainMenu.add_cascade(label="Fichier", menu=fileMenu, underline = 0)
        self.mainMenu.add_cascade(label="Journaux", menu=gestMenu, underline = 0, state = DISABLED)
        self.mainMenu.add_cascade(label="Messages", menu=msgMenu, underline = 0, state = DISABLED)
        self.mainMenu.add_cascade(label="Param�tres", menu=cfgMenu, underline = 0, state = DISABLED)
        self.mainMenu.add_cascade(label="Aide", underline = 0, menu=helpMenu)

        self.config(menu=self.mainMenu)
        

    def drawOthers(self):

        # variables locales
        vLigne = 0
        
        # Composants de la fen�tre
        texte = "..: Aide � la gestion d'une op�ration de secours avec r�seau d'urgence :.."
        self.tictac = StringVar()
        Label (self, text=texte, fg="blue", bg="orange", width=170).grid(row=vLigne, column=0, sticky=E+W)
        Label (self, textvariable=self.tictac, fg="blue", bg="orange", width=8).grid(row=vLigne, column=0, sticky=E)
        vLigne += 1

        self.notebook = Pmw.NoteBook(self, hull_width=1020, hull_height=510, 
                        createcommand = self.createTab, lowercommand = self.unselectTab, raisecommand = self.selectTab)
        self.notebook.grid(row = vLigne, column = 0)

    def createTab(self, page):
        """ Action � la cr�ation d'un onglet """
        
        if page == 'Gestion du R�seau':
            return
        elif page == 'Main Courante du Trafic':
            self.fenMCI.createTab()
        elif page == 'Log. Relev�s Sater':
            self.fenGSat.createTab()
        elif page == 'Log. Points Particuliers':
            self.fenGPoi.createTab()
        elif page == 'Liste des Victimes':
            self.fenGVict.createTab()
            
            
    def unselectTab(self, page):
        """ Action � la d�s�lection d'un onglet """

        if page == 'Gestion du R�seau':
            if self.fenRezo != None: self.fenRezo.unSelectTab()
        elif page == 'Main Courante du Trafic':
            if self.fenMCI != None: self.fenMCI.unSelectTab()
        elif page == 'Log. Relev�s Sater':
            if self.fenGSat != None: self.fenGSat.unSelectTab()
        elif page == 'Log. Points Particuliers':
            if self.fenGPoi != None: self.fenGPoi.unSelectTab()
        elif page == 'Liste des Victimes':
            if self.fenGVict != None: self.fenGVict.unSelectTab()
                
            
    def selectTab(self, page):
        """ Action � la s�lection d'un onglet """

        if page == 'Gestion du R�seau':
            if self.fenRezo != None: self.fenRezo.selectTab()
        elif page == 'Main Courante du Trafic':
            if self.fenMCI != None: self.fenMCI.selectTab()
        elif page == 'Log. Relev�s Sater':
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

    ### Fonction priv�e Timer ###
    def timer(self):
        self.tictac.set(time.strftime('%H:%M:%S'))
        self.after(1000, self.timer)

    ### Fonction priv�e d'appel de la fen�tre Config ###
    def newSess(self):
        vOldSess = self.userData['SESSION'].strip()
        # Sauvegarde de l'ancienne session
        if vOldSess != "":
            Session.writeSession(self)
            Reseau.writeReseau(self)
        # Nouvelle session
        Session.FormNewSess(self)
        # Si renseign�e, rafra�chissement de l'affichage
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
            self.mainMenu.entryconfigure("Param�tres", state = NORMAL)
            self.appelRes()

    def openSess(self):
        vOldSess = self.userData['SESSION'].strip()
        # Sauvegarde de l'ancienne session
        if vOldSess != "":
            Session.writeSession(self)
            Reseau.writeReseau(self)
        # Ouverture d'une session
        Session.openSess(self)
        # Si diff�rente, rafra�chissement de l'affichage
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
            self.mainMenu.entryconfigure("Param�tres", state = NORMAL)
            self.appelRes()
            
            
    ### Fonction priv�e d'appel de la fen�tre Config ###
    def appelCfg(self):
        Session.FormSession(self)


    ### Fonction priv�e d'appel de la fen�tre R�seau ###
    def appelRes(self):
        if self.fenRezo == None:
            self.fenRezo = Reseau.FormReseau(self)
        else:
            self.notebook.selectpage('Gestion du R�seau')

    ### Fonction priv�e d'appel de la fen�tre Aide ###
    def appelAbout(self):
        Help.FormAbout(self)

    ### Fonction priv�e d'appel de la fen�tre MCI ###
    def appelMCI(self):
        # Appel de la fen�tre Main Courante avec contr�le de son unicit� 
        if self.fenMCI == None :
            self.fenMCI = FormMCI(self)
        self.notebook.selectpage('Main Courante du Trafic')

    ### Fonction priv�e d'appel de la fen�tre GSAT ###
    def appelGSat(self):
        # Appel de la fen�tre Gestion Sater avec contr�le de son unicit� 
        if self.fenGSat == None :
            self.fenGSat = FormGSat(self)
        self.notebook.selectpage('Log. Relev�s Sater')

    ### Fonction priv�e d'appel de la fen�tre GPOI ###
    def appelGPoi(self):
        # Appel de la fen�tre Gestion POI avec contr�le de son unicit� 
        if self.fenGPoi == None :
            self.fenGPoi = FormGPoi(self)
        self.notebook.selectpage('Log. Points Particuliers')

    ### Fonction priv�e d'appel de la fen�tre GVict ###
    def appelGVict(self):
        # Appel de la fen�tre Gestion des Victimes avec contr�le de son unicit� 
        if self.fenGVict == None :
            self.fenGVict = FormGVict(self)
        self.notebook.selectpage('Liste des Victimes')

    ### Fonction priv�e d'appel de la fen�tre Gestion des Messages ###
    def appelGMsg(self):

        tkMessageBox.showinfo("Gestion des Messages", \
                              "Fonctionnalit� en cours de d�veloppement")
        return False

        # Appel de la fen�tre Main Courante avec contr�le de son unicit� 
        if self.fenGMsg == None :
            self.fenGMsg = FormGMsg(self, onglet)
        else :
            self.fenGMsg.fenetre.focus_set()

    ### Fonction priv�e d'appel de la fen�tre MCI ###
    def ouvrirMCI(self):
        tkMessageBox.showinfo("Gestion des Messages", \
                              "Fonctionnalit� en cours de d�veloppement")
        return False

    ### Fonction priv�e d'appel de la fen�tre OBNT ###
    def appelOBNT(self):
        FormOBNT(self)

    ### Fonction priv�e d'appel de la fen�tre IARU ###
    def appelIARU(self):
        FormIARU(self)

    ### Fonction priv�e d'appel de la fen�tre BT ###
    def appelMsgBT(self):
        FormBT(self)

    ### Fonction priv�e d'appel de la fen�tre DM ###
    def appelMsgDM(self):
        FormDM(self)

    ### Fonction priv�e d'appel de la fen�tre RMD ###
    def appelMsgRMD(self):
        FormRMD(self)

    ### Fonction priv�e d'appel de la fen�tre TMD ###
    def appelMsgTMD(self):
        FormTMD(self)

    ### Fonction priv�e d'appel de la fen�tre Bilan Secouriste ###
    def appelBilSec(self):
        FormBILSEC(self)

    ### Fonction priv�e d'appel de la fen�tre Bilan Ambiance ###
    def appelBilAmb(self):
        FormBilAmb(self)

    ### Fonction priv�e d'appel de la fen�tre POI ###
    def appelMsgPOI(self):
        FormPOI(self)

    ### Fonction priv�e d'appel de la fen�tre Sater ###
    def appelMsgSater(self):
        FormSATER(self)

    ### Fichier de Configuration ###
    def initCfgListe(self, ficCfg):
        "Alimente le dictionnaire de configuration avec des listes de valeurs"
        # Ouverture du fichier de configuration en mode lecture
        fic = open(ficCfg,'rb') 
        lignes = fic.readlines() ## R�cup�ration du contenu du fichier
        fic.close()
        for lig in lignes:
            sp = lig.split('#')[0] # Elimination des commentaires potentiels
            sp = lig.split('[')[0] # Elimination des sections
            sp = sp.split('=')     # S�paration variable sur le signe '=' valeur
            # on teste la longueur de sp;  si elle n'est pas �gale � 2, c'est qu'il s'agit d'une ligne vide ou qu'avec des commentaires
            if len(sp) == 2:
                cle   = sp[0].strip()
                liste = sp[1].strip().split(',')
                self.cfgListe[cle] = liste
        
    ### Fichier de Donn�es utilisateur ###
    def initUserData(self, ficUser):
        "Alimente le dictionnaire de configuration avec des valeurs du fichier"
        # Nettoyage du dictionnaire
        self.userData.clear()
        # Ouverture du fichier utilisateur en mode lecture
        # fic = open(ficUser,'rb') 
        lignes = ficUser.readlines() # R�cup�ration du contenu du fichier
        ficUser.close() 
        for lig in lignes:
            sp = lig.split('#')[0] # Elimination des commentaires potentiels
            sp = lig.split('[')[0] # Elimination des sections
            sp = sp.split('=')     # S�paration  des variables sur le signe '='
            # on teste la longueur de sp;  si elle n'est pas �gale � 2, c'est qu'il s'agit d'une ligne vide ou qu'avec des commentaires
            if len(sp) == 2:
                cle    = sp[0].strip()
                valeur = sp[1].strip()
                self.userData[cle] = valeur

    ### Fichier de Donn�es r�seau ###
    def initNetData(self, ficNet):
        "Alimente le dictionnaire des stations du r�seau avec des valeurs du fichier"
        # Nettoyage du dictionnaire
        self.netData.clear()
        # Ouverture du fichier utilisateur en mode lecture
        fic = open(ficNet,'rb') 
        lignes = fic.readlines() # R�cup�ration du contenu du fichier
        fic.close() 
        for lig in lignes:
            sp = lig.split('#')[0] # Elimination des commentaires potentiels
            sp = lig.split('[')[0] # Elimination des sections
            sp = sp.split('=')     # S�paration  des variables sur le signe '='
            # on teste la longueur de sp;  si elle n'est pas �gale � 2, c'est qu'il s'agit d'une ligne vide ou qu'avec des commentaires
            if len(sp) == 2:
                cle    = sp[0].strip()
                valeur = sp[1].strip()
                self.netData[cle] = valeur.decode("UTF-8")



################################
#  Lancement de l'application  #
#                              #
if __name__ == '__main__':
    gesADRA = MenuAdra()
    gesADRA.mainloop()
    exit
#                              #
################################
