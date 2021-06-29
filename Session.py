# -*- coding: iso-8859-15 -*-

from tkinter import *
from tkinter.scrolledtext import ScrolledText
 
import datetime
import time
import os
import tkinter.messagebox as tkMessageBox
import tkinter.filedialog as tkFileDialog
import Pmw
import sys

# Modules Techniques de GesADRA
import Commun            # Fonctions Principales
import Reseau

class FormNewSess(Toplevel):
    """Classe d�finissant le fen�tre 'Nouvelle Session'"""
    
    def __init__(self, appli):
        """Constructeur de la fen�tre NewSess"""
        
        self.root = appli
        # Nouvelle fen�tre pour Pmw
        Toplevel.__init__(self)
        Pmw.initialise()
        # Param�trage de la fen�tre
        if ( sys.platform.startswith('win')): 
            self.iconbitmap("appli.ico")
        self.resizable(width = False, height = False)
        self.wm_state()
        self.title ("Nouvelle Session")
        # C'est une fen�tre modale
        self.transient(self.root)
        self.grab_set() 
        self.focus_set()
        self.protocol("WM_DELETE_WINDOW", self.quitNewSess)
        # Instanciation d'une bulle d'aide
        self.bulle = Pmw.Balloon(self, relmouse = 'both')

        # Composants de la fen�tre
        vLigne = 1

        # Identification et choix de la session
        Label (self, text = "R�pertoire :").grid(row = vLigne, column = 0, sticky = W)
        self.efRepertoire = Pmw.EntryField (self)
        self.efRepertoire.grid(row = vLigne, column = 0, columnspan = 4, sticky = W+E)
        Button (self, text = "R�pertoire", command = self.changeRep, fg = "blue").grid (row = vLigne, column = 3)
        vLigne += 1
        Label (self, text = "Session ").grid(row = vLigne, column = 0, sticky = W)
        self.rbChoix = Pmw.RadioSelect(self, buttontype = "radiobutton", command=self.setControl, pady = 0)
        self.rbChoix.grid(row = vLigne, column = 1, sticky = W)
        self.rbChoix.add("standard")
        self.rbChoix.add("personnalis�e")
        self.efSession = Pmw.EntryField (self, validate = {"validator" : Commun.sessionValidator, "min" : 5, "max" : 15, "minstrict" : False, "maxstrict" : True})
        self.efSession.component('entry').bind('<Key>', Commun.uppercaseKey)
        self.efSession.grid(row = vLigne, column = 2, sticky = W+E)
        self.root.bulle.bind(self.efSession, "Session de 5 � 15 car. alphanum�riques (tiret et soulign� permis)")
        Button (self, text = "Cr�er", command = self.creerNewSess, fg = "red").grid (row = vLigne, column = 3, sticky = W+E)
        vLigne += 1

        self.efRepertoire.component('entry').config(state = DISABLED, bd = 0, disabledforeground="black")
        self.efRepertoire.setvalue(os.getcwd())
        self.rbChoix.invoke(0)

        self.wait_window()
        

    def setControl(self, tag):

        if tag == "standard":
            self.efSession.setvalue("S"+datetime.datetime.now().strftime("%Y%m%d"))
            self.efSession.component('entry').config(state = DISABLED, disabledforeground="black")
        else:
            self.efSession.component('entry').config(state = NORMAL)
            self.efSession.component('entry').focus_set()
            self.efSession.component('entry').selection_range(0, END)
            

    def creerNewSess(self):

        # Validation de la saisie
        if self.efSession.valid() == False:
            return False
        # Cr�ation du r�pertoire de session
        vSession = self.efSession.getvalue().strip()
        vRepSession = os.path.join(self.efRepertoire.getvalue(), vSession)
        if os.path.isdir(vRepSession) == False:
            os.mkdir(vRepSession)
            # Cr�ation du fichier de session 
            self.root.initUserData(open("GesADRA.ini", 'r'))   # Dico des donn�es utilisateur
            self.root.userData['REPTRAVAIL'] = vRepSession
            self.root.userData['SESSION'] = vSession
            self.root.userData['INTITULE'] += datetime.datetime.now().strftime(" %d/%m/%Y")
            writeSession(self)
            # Cr�ation du fichier r�seau
            self.root.initNetData("GesADRA.net")    # Dico des donn�es r�seau
            self.root.netData['STATION0'] = "TOUS"
            self.root.netData['OPERATEUR0'] = "Tous"
            for i in range(1,14): self.root.netData['STATUT'+str(i)] = "Inactif"
            Reseau.writeReseau(self)
            self.destroy()
        else :
            tkMessageBox.showerror("Erreur", "Cette session existe d�j�", parent=self)
            self.rbChoix.invoke(1)
    
    def quitNewSess(self):
        self.root.userData['SESSION'] = ""
        self.destroy()
    
    def changeRep(self):
        vDir = tkFileDialog.askdirectory(parent = self,
                                 title = "S�lectionnez le r�pertoire de travail",
                                 initialdir = self.efRepertoire.getvalue(),
                                 mustexist = False)
        if vDir != "":self.efRepertoire.setvalue (vDir)
                                 
def openSess(self):
    if os.path.isdir(os.path.join(Commun.getRepertoire(self), Commun.getSession(self))):
        vRep = os.path.join(Commun.getRepertoire(self), Commun.getSession(self))
    else: 
        vRep = Commun.getRepertoire(self)
        
    vFile = tkFileDialog.askopenfile(parent = self, 
                                    mode = 'r',
                                    title = "S�lectionnez le fichier de session � utiliser",
                                    initialdir = vRep,
                                    filetypes = [("Fichier ini", ".ini")],
                                    initialfile = "")
    
    if vFile != None:
        # Ouverture des fichiers en cours
        self.initUserData(vFile)
        # For�age
        self.userData['REPTRAVAIL'] = os.path.dirname(vFile.name)
        self.userData['SESSION'] = os.path.basename(vFile.name)[:-4]
        writeSession(self)
        self.initNetData(Commun.getFullPath(self, Commun.getFicReseau(self)))
   
 
class FormSession(Toplevel):
    """Classe d�finissant la fen�tre Param�trage"""
    
    def __init__(self, appli):
        """Constructeur de la fen�tre Param�trage"""

        # variables locales
        vLigne = 1 # N� de ligne pour le positionnement des composants
        self.root = appli
        # Nouvelle fen�tre pour Pmw
        Toplevel.__init__(self)
        Pmw.initialise()
        # Param�trage de la fen�tre
        if ( sys.platform.startswith('win')): 
            self.iconbitmap("appli.ico")
        self.resizable(width = False, height = False)
        self.wm_state()
        self.title ("Param�tres de Session")
        # C'est une fen�tre modale
        self.transient(self.root)
        self.grab_set() 
        self.focus_set()
        self.protocol("WM_DELETE_WINDOW", False)
        # Instanciation d'une bulle d'aide
        self.bulle = Pmw.Balloon(self, relmouse = 'both')

        # Composants de la fen�tre
        self.drawSession()
        self.initSession()

    def drawSession(self):

        # variables locales
        vLigne = 1

        Label (self, text = "Gestion de Session", fg = "blue",bg = "orange").grid(row = vLigne, column = 0, columnspan = 2, sticky = E+W)
        vLigne += 1

        # Identification et choix de la session
        Label (self, text = "Nom de Session :").grid(row = vLigne, column = 0, sticky = W)
        self.efSession = Pmw.EntryField (self, validate = {"min" : 7, "max" : 10, "minstrict" : False, "maxstrict" : True})
        self.efSession.grid(row = vLigne, column = 1, sticky = W+E)
        vLigne += 1
        Label (self, text = "Intitul� :").grid(row = vLigne, column = 0, sticky = W)
        self.efIntitule = Pmw.EntryField (self, validate = {"min" : 5, "max" : 30, "minstrict" : False, "maxstrict" : False})
        self.efIntitule.grid(row = vLigne, column = 1, sticky = W+E)
        vLigne += 1
        Label (self, text = "Activation : ").grid(row = vLigne, column = 0, sticky = W)
        self.cbActiv = Commun.comboWidget (self.root, self, self.root.cfgListe['Activer'])
        self.cbActiv.grid (row = vLigne, column = 1, sticky = E+W)    
        vLigne += 1

        Label (self, text = "Autres param�tres", fg = "blue",bg = "orange").grid(row = vLigne, column = 0, columnspan = 2, sticky = E+W)
        vLigne += 1

        notebook = Pmw.NoteBook(self)
        notebook.grid(row = vLigne, column = 0, columnspan = 2, sticky = W+E)
        
        # Onglet "Station locale"
        self.nbTab1 = notebook.add('Station locale')

        Label (self.nbTab1,text = "Indicatif : ").grid(row = vLigne, column = 0, sticky = W)
        self.efQrz = Pmw.EntryField(self.nbTab1, validate = {"validator" : Commun.nonVideValidator, "min" : 2, "max" : 8, "minstrict" : False, "maxstrict" : False})
        self.efQrz.grid (row = vLigne, column = 1, sticky = E+W)
        vLigne += 1

        Label (self.nbTab1,text = "Service : ").grid(row = vLigne, column = 0, sticky = W)
        self.eSrv = Entry (self.nbTab1)
        self.eSrv.grid (row = vLigne, column = 1, sticky = E+W)
        vLigne += 1

        Label (self.nbTab1,text = "Localisation (Ville) : ").grid(row = vLigne, column = 0, sticky = W)
        self.efVille = Pmw.EntryField(self.nbTab1, validate = Commun.nonVideValidator)
        self.efVille.grid (row = vLigne, column = 1, sticky = E+W)
        vLigne += 1

        Label (self.nbTab1, text = "D�partement : ").grid(row = vLigne, column = 0, sticky = W)
        self.eDept = Entry(self.nbTab1)
        self.eDept.grid (row = vLigne, column = 1, sticky = E+W)    
        vLigne += 1

        # Onglet "Fichiers LOG"
        self.nbTab2 = notebook.add('Fichiers LOG')
        
        Label (self.nbTab2,text = "Main Courante :").grid(row = vLigne, column = 0, sticky = W)
        self.eMCI = Entry (self.nbTab2)
        self.eMCI.grid (row = vLigne, column = 1, sticky = E+W)
        vLigne += 1

        Label (self.nbTab2,text = "Liste des Victimes :").grid(row = vLigne, column = 0, sticky = W)
        self.eVict = Entry (self.nbTab2)
        self.eVict.grid (row = vLigne, column = 1,sticky = E+W)
        vLigne += 1

        Label (self.nbTab2,text = "Relev�s SATER :").grid(row = vLigne, column = 0, sticky = W)
        self.eSater = Entry (self.nbTab2)
        self.eSater.grid (row = vLigne, column = 1, sticky = E+W)
        vLigne += 1

        Label (self.nbTab2,text = "Donn�es Carto. :").grid(row = vLigne, column = 0, sticky = W)
        self.eCarto = Entry (self.nbTab2)
        self.eCarto.grid (row = vLigne, column = 1, sticky = E+W)
        vLigne += 1

        # Onglet "Urgence Msg"
        self.nbTab3 = notebook.add("Urgence Msg")
        
        Label (self.nbTab3,text = "Standard OBNT :").grid(row = vLigne, column = 0, sticky = W)
        self.cbUrgOBNT = Commun.comboWidget (self.root, self.nbTab3, self.root.cfgListe['DegUrgOBNT'])
        self.cbUrgOBNT.grid (row = vLigne, column = 1, sticky = E+W)
        vLigne += 1

        Label (self.nbTab3,text = "Demande de Moyens :").grid(row = vLigne, column = 0, sticky = W)
        self.cbUrgDM = Commun.comboWidget (self.root, self.nbTab3, self.root.cfgListe['DegUrgOBNT'])
        self.cbUrgDM.grid (row = vLigne, column = 1,sticky = E+W)
        vLigne += 1

        Label (self.nbTab3,text = "Renseignement MD :").grid(row = vLigne, column = 0, sticky = W)
        self.cbUrgRMD = Commun.comboWidget (self.root, self.nbTab3, self.root.cfgListe['DegUrgOBNT'])
        self.cbUrgRMD.grid (row = vLigne, column = 1, sticky = E+W)
        vLigne += 1

        Label (self.nbTab3,text = "Transport MD :").grid(row = vLigne, column = 0, sticky = W)
        self.cbUrgTMD = Commun.comboWidget (self.root, self.nbTab3, self.root.cfgListe['DegUrgOBNT'])
        self.cbUrgTMD.grid (row = vLigne, column = 1, sticky = E+W)
        vLigne += 1

        Label (self.nbTab3,text = "Bilan d'Ambiance :").grid(row = vLigne, column = 0, sticky = W)
        self.cbUrgAMB = Commun.comboWidget (self.root, self.nbTab3, self.root.cfgListe['DegUrgOBNT'])
        self.cbUrgAMB.grid (row = vLigne, column = 1, sticky = E+W)
        vLigne += 1

        Label (self.nbTab3,text = "Bilan Secouriste :").grid(row = vLigne, column = 0, sticky = W)
        self.cbUrgSEC = Commun.comboWidget (self.root, self.nbTab3, self.root.cfgListe['DegUrg'])
        self.cbUrgSEC.grid (row = vLigne, column = 1,sticky = E+W)
        vLigne += 1

        Label (self.nbTab3,text = "Bilan Temporaire :").grid(row = vLigne, column = 0, sticky = W)
        self.cbUrgBT = Commun.comboWidget (self.root, self.nbTab3, self.root.cfgListe['DegUrgOBNT'])
        self.cbUrgBT.grid (row = vLigne, column = 1, sticky = E+W)
        vLigne += 1

        Label (self.nbTab3,text = "Relev� SATER :").grid(row = vLigne, column = 0, sticky = W)
        self.cbUrgSATER = Commun.comboWidget (self.root, self.nbTab3, self.root.cfgListe['DegUrgOBNT'])
        self.cbUrgSATER.grid (row = vLigne, column = 1, sticky = E+W)
        vLigne += 1

        Label (self.nbTab3,text = "Point Particulier :").grid(row = vLigne, column = 0, sticky = W)
        self.cbUrgPOI = Commun.comboWidget (self.root, self.nbTab3, self.root.cfgListe['DegUrgOBNT'])
        self.cbUrgPOI.grid (row = vLigne, column = 1, sticky = E+W)
        vLigne += 1

        # Onglet "Impression"
        self.nbTab4 = notebook.add("Impression")
        
        Label (self.nbTab4, text = "Impr. automatique des journaux : ").grid(row = vLigne, column = 0, sticky = W)
        self.rbImprLog = Pmw.RadioSelect(self.nbTab4, buttontype = "radiobutton")
        self.rbImprLog.grid(row = vLigne, column = 1, sticky = E)
        self.rbImprLog.add("NON")
        self.rbImprLog.add("OUI")
        vLigne += 1
        
        Label (self.nbTab4, text = "Impr. automatique des messages : ").grid(row = vLigne, column = 0, sticky = W)
        self.rbImprMsg = Pmw.RadioSelect(self.nbTab4, buttontype = "radiobutton")
        self.rbImprMsg.grid(row = vLigne, column = 1, sticky = E)
        self.rbImprMsg.add("NON")
        self.rbImprMsg.add("OUI")
        vLigne += 1

        Label (self.nbTab4, text = "Trace de main courante : ").grid(row = vLigne, column = 0, sticky = W)
        self.rbTrace = Pmw.RadioSelect(self.nbTab4, buttontype = "radiobutton")
        self.rbTrace.grid(row = vLigne, column = 1, sticky = W)
        self.rbTrace.add("NON")
        self.rbTrace.add("OUI")
        vLigne += 1

        notebook.setnaturalsize()
        Label (self, text = "", fg = "blue",bg = "orange").grid(row = vLigne, column = 0, columnspan = 2, sticky = E+W)
        vLigne += 1

        Button (self, text = "Enregistrer", width = 14, command = self.saveSession, fg = "red").grid (row = vLigne, column = 0)
        Button (self, text = "Quitter", width = 14, command = self.destroy, fg = "red").grid (row = vLigne, column = 1)


    def initSession(self):
        
        self.efSession.setvalue(Commun.getSession(self.root))
        self.efSession.component('entry').config(state = DISABLED)
        self.efIntitule.setvalue(self.root.userData['INTITULE']) 
        self.cbActiv.selectitem(self.root.userData['ACTIVATION'])
            
        self.efQrz.setvalue(self.root.userData['INDICATIF']) # Indicatif station
        self.efVille.setvalue(self.root.userData['LOCALITE']) # Ville
        self.eSrv.insert(0, self.root.userData['SERVICE']) # Indicatif station
        self.eDept.insert(0, self.root.userData['LIB_DPT']) # Indicatif station
        self.eMCI.insert(0,Commun.getFicMCI(self.root))
        self.eVict.insert(0,Commun.getFicGVict(self.root))
        self.eSater.insert(0,Commun.getFicGSat(self.root))
        self.eCarto.insert(0,Commun.getFicGPoi(self.root))
        self.cbUrgOBNT.selectitem(self.root.userData['URG_OBNT'])
        self.cbUrgDM.selectitem(self.root.userData['URG_DM'])
        self.cbUrgRMD.selectitem(self.root.userData['URG_RMD'])
        self.cbUrgTMD.selectitem(self.root.userData['URG_TMD'])
        self.cbUrgAMB.selectitem(self.root.userData['URG_BILAMB'])
        self.cbUrgSEC.selectitem(self.root.userData['URG_BILSEC'])
        self.cbUrgBT.selectitem(self.root.userData['URG_BT'])
        self.cbUrgSATER.selectitem(self.root.userData['URG_SATER'])
        self.cbUrgPOI.selectitem(self.root.userData['URG_POI'])
        vImprLog = self.root.userData['IMPR_LOG']
        self.rbImprLog.invoke(vImprLog) # Demande d'impression des messages
        vImprMsg = self.root.userData['IMPR_MSG']
        self.rbImprMsg.invoke(vImprMsg) # Demande d'impression des messages
        vTrace = self.root.userData['TRACE']
        self.rbTrace.invoke(vTrace) # Demande d'impression des traces
        

    def saveSession(self):

        # Appliquer les modifs dans le dictionnaire
        # Session en cours
        # self.root.userData['SESSION'] = self.efSession.getvalue()
        self.root.userData['INTITULE'] = self.efIntitule.getvalue()
        self.root.userData['ACTIVATION'] = self.cbActiv.get()

        # Station directrice
        self.root.userData['INDICATIF'] = self.efQrz.getvalue().upper()
        self.root.userData['LOCALITE'] = self.efVille.getvalue().upper()
        self.root.userData['SERVICE'] = self.eSrv.get().upper()
        self.root.userData['LIB_DPT'] = self.eDept.get().upper()

        # Fichiers par d�faut
        self.root.userData['FIC_MCI'] = self.eMCI.get()
        self.root.userData['FIC_VICT'] = self.eVict.get()
        self.root.userData['FIC_SATER'] = self.eSater.get()
        self.root.userData['FIC_CARTO'] = self.eCarto.get()

        # Degr�s d'Urgence
        self.root.userData['URG_OBNT'] = self.cbUrgOBNT.get()
        self.root.userData['URG_DM'] = self.cbUrgDM.get()
        self.root.userData['URG_RMD'] = self.cbUrgRMD.get()
        self.root.userData['URG_TMD'] = self.cbUrgTMD.get()
        self.root.userData['URG_BILAMB'] = self.cbUrgAMB.get()
        self.root.userData['URG_BILSEC'] = self.cbUrgSEC.get()
        self.root.userData['URG_BT'] = self.cbUrgBT.get()
        self.root.userData['URG_SATER'] = self.cbUrgSATER.get()
        self.root.userData['URG_POI'] = self.cbUrgPOI.get()
        
        # Impression des journaux   
        self.root.userData['IMPR_LOG'] = self.rbImprLog.getcurselection()
        # Impression des messages   
        self.root.userData['IMPR_MSG'] = self.rbImprMsg.getcurselection()
        # Impression de la trace   
        self.root.userData['TRACE'] = self.rbTrace.getcurselection()
        # Enregistrer les modifs dans le fichier de session
        writeSession(self)

        # Fermer la fenetre
        self.destroy()
        return
#
#
def writeSession(self):
    """Sauvegarde des param�tres de session""" 
    vData = []
    for cle, valeur in self.root.userData.items():
        vData.append(cle + " = " + valeur+"\n")
    fic = open(Commun.getFullPath(self.root,Commun.getFicSession(self.root)), 'w')
    fic.writelines(vData)
    fic.close()

