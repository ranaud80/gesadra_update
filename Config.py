# -*- coding: iso-8859-15 -*-

from Tkinter import *
from ScrolledText import ScrolledText
 
import datetime
import time
import os
import shutil
import tkMessageBox
import tkSimpleDialog
import tkFileDialog
import Pmw
import sys

# Modules Techniques de GesADRA
import Commun            # Fonctions Principales
import Reseau

class FormParam:
    """Classe définissant la fenêtre Paramétrage"""
    
    def __init__(self, appli, nouvelleSession):
        """Constructeur de la fenêtre Paramétrage"""

        # variables locales
        vLigne = 1 # N° de ligne pour le positionnement des composants

        # Nouvelle fenêtre pour Pmw
        vFen = Toplevel(appli.fenPpale)
        Pmw.initialise(vFen)
        # vFen est une fenêtre modale
        vFen.grab_set() 
        vFen.focus_set()
        # Paramétrage de la fenêtre
        vFen.iconbitmap("appli.ico")
        vFen.resizable(width = False, height = False)
        vFen.wm_state()
        vFen.title ("Paramétrage de " + appli.userData['LOGICIEL']+ " " + appli.userData['VERSION'])
        # Instanciation d'une bulle d'aide
        vFen.bulle = Pmw.Balloon(vFen, relmouse = 'both')
        # Fermeture par la case système interdite
        vFen.protocol("WM_DELETE_WINDOW", False)
        # Référence sur la nouvelle fenêtre 
        self.vFen = vFen

        # Composants de la fenêtre
        self.dessineParam(appli)
   
        # Mise en forme de la fenêtre
        if nouvelleSession == True:
            # Montrer les boutons Nouveau/Reprise, cacher les autres informations
            self.fNew.grid()
            self.fStd.grid_remove()
            # Initialisations effectuées plus loin
        else:
            # et l'inverse
            self.fNew.grid_remove()
            self.fStd.grid()
            # Initialisations
            self.initChamps(appli) 


    def dessineParam(self, appli):

        # variables locales
        vFen = self.vFen
        # self.reseau = [] # liste des stations du réseau   
        # self.reseau.append("TOUS") # la station 0 est "TOUS"
        vLigne = 1

        Label (vFen, text = "Gestion de Session", fg = "blue",bg = "orange").grid(row = vLigne, column = 0, columnspan = 2, sticky = E+W)
        vLigne = vLigne +1

        # Identification et choix de la session
        Label (vFen, text = "Nom de Session :").grid(row = vLigne, column = 0, sticky = W)
        self.efSession = Pmw.EntryField (vFen, validate = {"min" : 9, "max" : 10, "minstrict" : False, "maxstrict" : True})
        self.efSession.grid(row = vLigne, column = 1, sticky = W+E)
        vLigne = vLigne + 1
        Label (vFen, text = "Intitulé :").grid(row = vLigne, column = 0, sticky = W)
        self.efIntitule = Pmw.EntryField (vFen, validate = {"min" : 5, "max" : 30, "minstrict" : False, "maxstrict" : False})
        self.efIntitule.grid(row = vLigne, column = 1, sticky = W+E)
        vLigne = vLigne +1
        Label (vFen, text = "Activation : ").grid(row = vLigne, column = 0, sticky = W)
        self.cbActiv = Commun.comboWidget (vFen, vFen, appli.cfgListe['Activer'])
        self.cbActiv.grid (row = vLigne, column = 1, sticky = E+W)    
        vLigne = vLigne +1

        # Frame contenant les boutons Nouveau/Reprise
        self.fNew = Frame(vFen)
        self.fNew.grid(row = vLigne, column = 0, columnspan = 2)
        Button (self.fNew, text = "Nouvelle session", command = lambda : self.creerSession(appli), fg = "blue", width = 29).grid (row = vLigne, column = 0)
        Button (self.fNew, text = "Reprise de session", command = lambda : self.changerSession(appli), fg = "blue", width = 29).grid (row = vLigne, column = 1)
        vLigne = vLigne + 1

        # Frame contenant les informations de session
        self.fStd = Frame (vFen)
        self.fStd.grid(row = vLigne, column = 0, columnspan = 2)

        Label (self.fStd, text = "Station locale", fg = "blue",bg = "orange").grid(row = vLigne, column = 0, columnspan = 2, sticky = E+W)
        vLigne = vLigne +1

        Label (self.fStd,text = "Indicatif de votre station : ").grid(row = vLigne, column = 0, sticky = W)
        self.efQrz = Pmw.EntryField(self.fStd, validate = {"validator" : Commun.nonVideValidator, "min" : 2, "max" : 8, "minstrict" : False, "maxstrict" : False})
        self.efQrz.grid (row = vLigne, column = 1, sticky = E+W)
        vLigne = vLigne +1

        Label (self.fStd,text = "Localisation (Ville) : ").grid(row = vLigne, column = 0, sticky = W)
        self.efVille = Pmw.EntryField(self.fStd, validate = Commun.nonVideValidator)
        self.efVille.grid (row = vLigne, column = 1, sticky = E+W)
        vLigne = vLigne +1

        Label (self.fStd,text = "Service : ").grid(row = vLigne, column = 0, sticky = W)
        self.eSrv = Entry (self.fStd)
        self.eSrv.grid (row = vLigne, column = 1, sticky = E+W)
        vLigne = vLigne +1

        Label (self.fStd, text = "Département : ").grid(row = vLigne, column = 0, sticky = W)
        self.eDept = Entry(self.fStd)
        self.eDept.grid (row = vLigne, column = 1, sticky = E+W)    
        vLigne = vLigne +1

        Label (self.fStd, text = "Autres paramètres", fg = "blue",bg = "orange").grid(row = vLigne, column = 0, columnspan = 2, sticky = E+W)
        vLigne = vLigne +1

        self.iDefFic = IntVar()
        self.ckDefFic = Checkbutton (self.fStd, text = 'Modifier les noms de fichiers "log"', variable = self.iDefFic, command = self.cocherDefFic)
        self.ckDefFic.grid(row = vLigne, column = 0, columnspan = 3, sticky = W)
        vLigne = vLigne+1

        # sous-frame spécifique pour les fichiers CSV
        self.fFic = Frame(self.fStd)
        self.fFic.grid(row = vLigne, column = 0, columnspan = 2)
        Label (self.fFic,text = "Fichier Main Courante :").grid(row = vLigne, column = 0, sticky = W)
        self.eMCI = Entry (self.fFic)
        self.eMCI.grid (row = vLigne, column = 1, sticky = E+W)
        vLigne = vLigne+1

        Label (self.fFic,text = "Fichier des Victimes :").grid(row = vLigne, column = 0, sticky = W)
        self.eVict = Entry (self.fFic)
        self.eVict.grid (row = vLigne, column = 1,sticky = E+W)
        vLigne = vLigne+1

        Label (self.fFic,text = "Fichier Relevés SATER :").grid(row = vLigne, column = 0, sticky = W)
        self.eSater = Entry (self.fFic)
        self.eSater.grid (row = vLigne, column = 1, sticky = E+W)
        vLigne = vLigne+1

        Label (self.fFic,text = "Fichier Cartographie :").grid(row = vLigne, column = 0, sticky = W)
        self.eCarto = Entry (self.fFic)
        self.eCarto.grid (row = vLigne, column = 1, sticky = E+W)
        vLigne = vLigne+1

        self.iDefUrg = IntVar()
        self.ckDefUrg = Checkbutton (self.fStd, text = "Modifier les Degrés d'Urgence des messages", variable = self.iDefUrg, command = self.cocherDefUrg)
        self.ckDefUrg.grid(row = vLigne, column = 0, columnspan = 3, sticky = W)
        vLigne = vLigne+1

        # sous-frame spécifique pour les Degrés d'Urgence
        self.fUrg = Frame(self.fStd)
        self.fUrg.grid(row = vLigne, column = 0, columnspan = 2)
        Label (self.fUrg,text = "Standard OBNT :").grid(row = vLigne, column = 0, sticky = W)
        self.cbUrgOBNT = Commun.comboWidget (vFen, self.fUrg, appli.cfgListe['DegUrgOBNT'])
        self.cbUrgOBNT.grid (row = vLigne, column = 1, sticky = E+W)
        vLigne = vLigne+1

        Label (self.fUrg,text = "Demande de Moyens :").grid(row = vLigne, column = 0, sticky = W)
        self.cbUrgDM = Commun.comboWidget (vFen, self.fUrg, appli.cfgListe['DegUrgOBNT'])
        self.cbUrgDM.grid (row = vLigne, column = 1,sticky = E+W)
        vLigne = vLigne+1

        Label (self.fUrg,text = "Renseignement MD :").grid(row = vLigne, column = 0, sticky = W)
        self.cbUrgRMD = Commun.comboWidget (vFen, self.fUrg, appli.cfgListe['DegUrgOBNT'])
        self.cbUrgRMD.grid (row = vLigne, column = 1, sticky = E+W)
        vLigne = vLigne+1

        Label (self.fUrg,text = "Transport MD :").grid(row = vLigne, column = 0, sticky = W)
        self.cbUrgTMD = Commun.comboWidget (vFen, self.fUrg, appli.cfgListe['DegUrgOBNT'])
        self.cbUrgTMD.grid (row = vLigne, column = 1, sticky = E+W)
        vLigne = vLigne+1

        Label (self.fUrg,text = "Bilan d'Ambiance :").grid(row = vLigne, column = 0, sticky = W)
        self.cbUrgAMB = Commun.comboWidget (vFen, self.fUrg, appli.cfgListe['DegUrgOBNT'])
        self.cbUrgAMB.grid (row = vLigne, column = 1, sticky = E+W)
        vLigne = vLigne+1

        Label (self.fUrg,text = "Bilan Secouriste :").grid(row = vLigne, column = 0, sticky = W)
        self.cbUrgSEC = Commun.comboWidget (vFen, self.fUrg, appli.cfgListe['DegUrg'])
        self.cbUrgSEC.grid (row = vLigne, column = 1,sticky = E+W)
        vLigne = vLigne+1

        Label (self.fUrg,text = "Bilan Temporaire :").grid(row = vLigne, column = 0, sticky = W)
        self.cbUrgBT = Commun.comboWidget (vFen, self.fUrg, appli.cfgListe['DegUrgOBNT'])
        self.cbUrgBT.grid (row = vLigne, column = 1, sticky = E+W)
        vLigne = vLigne+1

        Label (self.fUrg,text = "Relevé SATER :").grid(row = vLigne, column = 0, sticky = W)
        self.cbUrgSATER = Commun.comboWidget (vFen, self.fUrg, appli.cfgListe['DegUrgOBNT'])
        self.cbUrgSATER.grid (row = vLigne, column = 1, sticky = E+W)
        vLigne = vLigne+1

        Label (self.fUrg,text = "Point Particulier :").grid(row = vLigne, column = 0, sticky = W)
        self.cbUrgPOI = Commun.comboWidget (vFen, self.fUrg, appli.cfgListe['DegUrgOBNT'])
        self.cbUrgPOI.grid (row = vLigne, column = 1, sticky = E+W)
        vLigne = vLigne+1

        Label (self.fStd, text = "Impression automatique des messages : ").grid(row = vLigne, column = 0, sticky = W)
        self.rbImpr = Pmw.RadioSelect(self.fStd, buttontype = "radiobutton")
        self.rbImpr.grid(row = vLigne, column = 1, sticky = E)
        self.rbImpr.add("NON")
        self.rbImpr.add("OUI")
        vLigne = vLigne +1

        Label (self.fStd, text = "Impression d'une trace de main courante : ").grid(row = vLigne, column = 0, sticky = W)
        self.rbTrace = Pmw.RadioSelect(self.fStd, buttontype = "radiobutton")
        self.rbTrace.grid(row = vLigne, column = 1, sticky = W)
        self.rbTrace.add("NON")
        self.rbTrace.add("OUI")
        vLigne = vLigne +1

        Label (self.fStd, text = "", fg = "blue",bg = "orange").grid(row = vLigne, column = 0, columnspan = 2, sticky = E+W)
        vLigne = vLigne +1

        Button (self.fStd, text = "Enregistrer", width = 14, command = lambda : self.enregistrer(appli), fg = "red").grid (row = vLigne, column = 0)
        Button (self.fStd, text = "Quitter", width = 14, command = lambda : self.vFen.destroy(), fg = "red").grid (row = vLigne, column = 1)


    def initChamps(self, appli):
        
        self.efSession.setvalue(Commun.getSession(appli))
        self.efIntitule.setvalue(appli.userData['INTITULE']) 
        self.cbActiv.selectitem(appli.userData['ACTIVATION'])
            
        self.efQrz.setvalue(appli.userData['INDICATIF']) # Indicatif station
        self.efVille.setvalue(appli.userData['LOCALITE']) # Ville
        self.eSrv.insert(0, appli.userData['SERVICE']) # Indicatif station
        self.eDept.insert(0, appli.userData['LIB_DPT']) # Indicatif station
        self.iDefFic.set(False) 
        self.cocherDefFic() # Cocher pour masquer les fichiers
        self.eMCI.insert(0,Commun.getFicMCI(appli))
        self.eVict.insert(0,Commun.getFicGVict(appli))
        self.eSater.insert(0,Commun.getFicGSat(appli))
        self.eCarto.insert(0,Commun.getFicGPoi(appli))
        self.iDefUrg.set(False) 
        self.cocherDefUrg() # Cocher pour masquer les fichiers
        self.cbUrgOBNT.selectitem(appli.userData['URG_OBNT'])
        self.cbUrgDM.selectitem(appli.userData['URG_DM'])
        self.cbUrgRMD.selectitem(appli.userData['URG_RMD'])
        self.cbUrgTMD.selectitem(appli.userData['URG_TMD'])
        self.cbUrgAMB.selectitem(appli.userData['URG_BILAMB'])
        self.cbUrgSEC.selectitem(appli.userData['URG_BILSEC'])
        self.cbUrgBT.selectitem(appli.userData['URG_BT'])
        self.cbUrgSATER.selectitem(appli.userData['URG_SATER'])
        self.cbUrgPOI.selectitem(appli.userData['URG_POI'])
        vImpr = appli.userData['IMPRESSION']
        self.rbImpr.invoke(vImpr) # Demande d'impression des messages
        vTrace = appli.userData['TRACE']
        self.rbTrace.invoke(vTrace) # Demande d'impression des traces
        

    def cocherDefFic(self):
        # Cacher / Montrer la frame
        if self.iDefFic.get() == False:
            self.fFic.grid_remove()
        else:
            self.fFic.grid()


    def cocherDefUrg(self):
        # Cacher / Montrer la frame
        if self.iDefUrg.get() == False:
            self.fUrg.grid_remove()
        else:
            self.fUrg.grid()


    def creerSession(self, appli):

        # Validation de la saisie
        if self.efSession.valid() == False or self.efIntitule.valid() == False:
            return False
        # Création du répertoire de session
        vSession = self.efSession.getvalue().upper().strip()
        vRepSession = os.path.join(os.getcwd(), vSession)
        if os.path.isdir(vRepSession) == False:
            os.mkdir(vRepSession)
            # Création du fichier de session 
            appli.userData['SESSION'] = vSession
            appli.userData['INTITULE'] = self.efIntitule.getvalue().strip()
            appli.userData['ACTIVATION'] = self.cbActiv.get()
            # initialisation des champs
            self.initChamps(appli)
            sauveSession(appli)
            Reseau.sauveReseau(appli)
            self.fNew.grid_remove()
            self.fStd.grid()
        else :
            tkMessageBox.showinfo("Erreur", "Cette session existe déjà")
    
        
    def changerSession(self, appli):

        vDir = tkFileDialog.askdirectory(parent = self.vFen,
                                         title = "Sélectionnez le répertoire de la session à utiliser",
                                         initialdir = Commun.getRepertoire(),
                                         mustexist = True)
        vFic = vDir + vDir[vDir.rfind("/"):]
        if os.path.isfile(vFic+".ini") == True:
            # Ouverture des fichiers en cours
            appli.initUserData(Commun.getFullPath(appli, vFic + ".ini"))
            appli.initNetData(Commun.getFullPath(appli, vFic + ".net"))
            # initialisation des champs
            self.initChamps(appli)
            # Masquer les boutons Nouveau/Reprise et montrer les informations
            self.fNew.grid_remove()
            self.fStd.grid()
        else:
            tkMessageBox.showinfo("Erreur", "Ce répertoire ne contient pas de session valide")

        
    def enregistrer(self, appli):

        # Appliquer les modifs dans le dictionnaire
        # Session en cours
        appli.userData['SESSION'] = self.efSession.getvalue()
        appli.userData['INTITULE'] = self.efIntitule.getvalue()
        appli.userData['ACTIVATION'] = self.cbActiv.get()

        # Station directrice
        appli.userData['INDICATIF'] = self.efQrz.getvalue().upper()
        appli.userData['LOCALITE'] = self.efVille.getvalue().upper()
        appli.userData['SERVICE'] = self.eSrv.get().upper()
        appli.userData['LIB_DPT'] = self.eDept.get().upper()

        # Fichiers par défaut
        if self.iDefFic.get() == True :
            appli.userData['FIC_MCI'] = self.eMCI.get()
            appli.userData['FIC_VICT'] = self.eVict.get()
            appli.userData['FIC_SATER'] = self.eSater.get()
            appli.userData['FIC_CARTO'] = self.eCarto.get()
        # Degrés d'Urgence
        if self.iDefUrg.get() == True :
            appli.userData['URG_OBNT'] = self.cbUrgOBNT.get()
            appli.userData['URG_DM'] = self.cbUrgDM.get()
            appli.userData['URG_RMD'] = self.cbUrgRMD.get()
            appli.userData['URG_TMD'] = self.cbUrgTMD.get()
            appli.userData['URG_BILAMB'] = self.cbUrgAMB.get()
            appli.userData['URG_BILSEC'] = self.cbUrgSEC.get()
            appli.userData['URG_BT'] = self.cbUrgBT.get()
            appli.userData['URG_SATER'] = self.cbUrgSATER.get()
            appli.userData['URG_POI'] = self.cbUrgPOI.get()
        
        # Impression des messages   
        appli.userData['IMPRESSION'] = self.rbImpr.getcurselection()
        # Impression de la trace   
        appli.userData['TRACE'] = self.rbTrace.getcurselection()
        # Enregistrer les modifs dans le fichier de session
        sauveSession(appli)

        # Mettre à jour la fenêtre principale
        appli.initMenuADRA()  

        # Fermer la fenetre
        self.vFen.destroy()
        return
#
#
def initSession(appli):
    """Initialisation de la session courante de GesADRA"""

    vTitre = appli.userData['LOGICIEL']+" "+appli.userData['VERSION']

    # Test de la présence du fichier de session pour la date du jour
    vChemin = Commun.getFullPath(appli, "")
    vFicSession = Commun.getFullPath(appli, Commun.getFicSession(appli))
    vFicReseau  = Commun.getFullPath(appli, Commun.getFicReseau(appli))

    if os.path.isfile(vFicSession) == True:
        vMsg = "Reprise de session : \n Voulez-vous utiliser la session "+Commun.getSession(appli)+" en cours ?"
        if tkMessageBox.askyesno(vTitre, vMsg):
            # Ouverture des fichiers en cours
            appli.initUserData(Commun.getFullPath(appli,vFicSession))
            appli.initNetData (Commun.getFullPath(appli,vFicReseau))
        else:
            # fenêtre de configuration
            FormParam(appli, True)
    else:
        vMsg = "Nouvelle session : \n Voulez-vous utiliser les paramètres par défaut ?"
        if tkMessageBox.askyesno(vTitre, vMsg):
            # Création du répertoire de session
            os.mkdir(vChemin)
            # Création du fichier par défault à partir des éléments de GesADRA.ini
            appli.userData['INTITULE'] = appli.userData['INTITULE'] + " " + datetime.datetime.now().strftime("%d/%m/%Y")
            sauveSession(appli)
            Reseau.sauveReseau(appli)
        else:
            # fenêtre de configuration
            FormParam(appli, True)

def sauveSession(appli):
    """Sauvegarde des paramètres de session""" 
    vData = []
    for cle, valeur in appli.userData.items():
        vData.append(cle + " = " + valeur+"\n")
    fic = open(Commun.getFullPath(appli,Commun.getFicSession(appli)), 'w')
    fic.writelines(vData)
    fic.close()

