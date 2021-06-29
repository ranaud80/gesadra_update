# -*- coding: iso-8859-15 -*-

from tkinter import *
from tkinter.scrolledtext import ScrolledText

import datetime
import time
import os
import tkinter.messagebox as tkMessageBox
import tkinter.font as tkFont
import Pmw
import Commun # Module principal des fonctions annexes
 
###################### Creation d'un message Bilan Temporaire.
class FormBILSEC:
    "Classe définissant le formulaire Bilan Secouriste"

    
    def __init__(self, appli):
        "Constructeur de la fenêtre Bilan Secouriste"

        self.root = appli # Référence à l'application racine

        self.ligneLesion = [] # Tableau des lignes "lésion"
        self.listeCkLesion = [] # Tableau des valeurs cochées par ligne "lésion"
	
        # Création de la nouvelle fenêtre
        self.fenetre = Commun.nouvelleFenetre(self.root, "Bilan Secouriste")
        # Fermeture par la case système
        self.fenetre.protocol("WM_DELETE_WINDOW", self.quitterBILSEC)

        # Composants de la fenêtre
        self.dessineBILSEC()
        self.bulleAide()
        
        # Initialisations
        self.razSaisie()
        
        # Gestion des raccourcis clavier
        self.fenetre.bind('<Alt-v>', self.validerBILSEC)
        self.fenetre.bind('<Return>', self.validerBILSEC)
        self.fenetre.bind('<Alt-n>', self.annulerBILSEC)
        self.fenetre.bind('<Escape>', self.annulerBILSEC)
        self.fenetre.bind('<Alt-q>', self.quitterBILSEC)
        self.stCirc.bind('<Return>', self.notReturn1) # On ne valide pas par <Entrée> sur la zone stCirc
        self.stGestes.bind('<Return>', self.notReturn2) # On ne valide pas par <Entrée> sur la zone stGestes
        self.stSoins.bind('<Return>', self.notReturn3) # On ne valide pas par <Entrée> sur la zone stSoins


    def dessineBILSEC(self):

        # variables locales
        vLigne = 1 # N° de ligne pour le positionnement des composants
        vFen = self.fenetre

        # Composants de la fenêtre
        Label (vFen,text = "Informations transmission", fg = "blue",bg = "orange").grid(row = vLigne, column = 0, columnspan = 9, sticky = E+W)
        vLigne += 1

        Label (vFen, text = "Groupe Date/Heure : ").grid(row = vLigne, column = 0, sticky = W)
        self.efGdh = Commun.gdhWidget(vFen, vFen)
        self.efGdh.grid(row = vLigne, column = 1, columnspan = 2,sticky = W)
        self.iGdh = IntVar()
        self.ckGdh = Checkbutton (vFen, text = "Recalculer le GDH lors de la validation", variable = self.iGdh)
        self.ckGdh.grid(row = vLigne, column = 3, columnspan = 3, sticky = W)
        vLigne += 1
        Label (vFen, text = "Emis par : ").grid(row = vLigne, column = 0, sticky = W)
        self.cbEmetteur = Commun.indicatifWidget(vFen, vFen, self.root)
        self.cbEmetteur.grid (row = vLigne, column = 1, columnspan = 2, sticky = W)
        Label (vFen, text = "Reçu par : ").grid(row = vLigne, column = 3, sticky = W)
        self.cbDestinataire = Commun.indicatifWidget(vFen, vFen, self.root)
        self.cbDestinataire.grid (row = vLigne, column = 4, columnspan = 2, sticky = W)
        vLigne += 1
        Label (vFen, text = "Instructions particulières : ").grid(row = vLigne, column = 0, sticky = W)
        self.eInstruc = Entry (vFen)
        self.eInstruc.grid (row = vLigne, column = 1, columnspan = 6, sticky = W+E)
        vLigne += 1

        Label (vFen, text = "Bilan Secouriste", fg = "blue",bg = "orange").grid(row = vLigne, column = 0, columnspan = 9, sticky = W+E)
        vLigne += 1

        Label (vFen, text = "Entête du message", fg = "blue",bg = "cyan").grid(row = vLigne, column = 0, columnspan = 9, sticky = E+W)
        vLigne += 1
        Label (vFen, text = "Origine : ").grid(row = vLigne, column = 0, sticky = W)
        self.efOrigine = Pmw.EntryField (vFen, validate = Commun.nonVideValidator)
        self.efOrigine.grid (row = vLigne, column = 1 ,sticky = W)
        vLigne += 1
        Label (vFen, text = "Destinataires Action : ").grid(row = vLigne, column = 0, sticky = W)
        self.efDestAction = Pmw.EntryField (vFen, validate = Commun.nonVideValidator)
        self.efDestAction.grid (row = vLigne, column = 1, columnspan = 4, sticky = E+W)
        Label (vFen, text = "(utilisez le / comme séparateur)").grid(row = vLigne, rowspan = 2, column = 5, columnspan = 3, sticky = W)
        vLigne += 1
        Label (vFen, text = "Destinataires Info : ").grid(row = vLigne, column = 0, sticky = W)
        self.eDestInfo = Entry (vFen)
        self.eDestInfo.grid (row = vLigne, column = 1, columnspan = 4, sticky = E+W)
        vLigne += 1
        Label (vFen, text = "Degré d'Urgence : ").grid(row = vLigne, column = 0, sticky = W )
        self.cbDegUrg = Commun.comboWidget (self.root, vFen, self.root.cfgListe['DegUrg'])
        self.cbDegUrg.grid (row = vLigne, column = 1, columnspan = 2, sticky = W)
        vLigne += 1

        Label (vFen,text = "Corps de message", fg = "blue",bg = "cyan").grid(row = vLigne, column = 0,columnspan = 9, sticky = W+E)
        vLigne += 1
        self.notebook = Pmw.NoteBook(vFen)
        self.notebook.grid(row = vLigne, column = 0, columnspan = 9, sticky = W+E)
        self.nbTab1 = self.notebook.add('Bilan Circonstancié')
        self.nbTab1.grid_columnconfigure(0, weight=2)
        self.nbTab1.grid_columnconfigure(2, weight=1)
        self.nbTab1.grid_columnconfigure(3, weight=2)
        self.nbTab1.grid_columnconfigure(5, weight=1)
        self.nbTab1.grid_columnconfigure(6, weight=2)
        self.nbTab1.grid_columnconfigure(8, weight=2)
        
       # Victime
        Label (self.nbTab1,text = "Identité de la Victime", fg = "blue", bg = "darkgrey").grid(row = vLigne, column = 0,columnspan = 9, sticky = W+E)
        vLigne += 1
        Label (self.nbTab1, text = "Num Victime (ou dossard) : ").grid(row = vLigne, column = 0, sticky = W) 
        self.efNum = Pmw.EntryField (self.nbTab1, validate = Commun.nonVideValidator)
        self.efNum.component('entry').config(width = 8) 
        self.efNum.grid(row = vLigne, column = 1, sticky = W) 
        self.bNum = Button(self.nbTab1, width = 8, bd = 1, fg = "blue", text = "Num. Auto", command = self.numAuto, underline = 0)
        self.bNum.grid(row = vLigne, column = 2)
        Label (self.nbTab1, text = "Age / Date de naissance :").grid(row = vLigne, column = 3, sticky = W)
        self.eAge = Entry(self.nbTab1)
        self.eAge.grid (row = vLigne, column = 4, sticky = W)
        Label (self.nbTab1, text = "Sexe :").grid(row = vLigne, column = 6, sticky = W)
        self.rbSexe = Pmw.RadioSelect(self.nbTab1, buttontype = "radiobutton", pady = 0)
        self.rbSexe.grid(row = vLigne, column = 7, sticky = W)
        self.rbSexe.add("H")
        self.rbSexe.add("F")
        vLigne += 1
        Label (self.nbTab1, text = "Nom - Prénom :").grid(row = vLigne, column = 0, sticky = W)
        self.eNom = Entry(self.nbTab1)
        self.eNom.grid(row = vLigne, column = 1, columnspan = 4, sticky = W+E)
        vLigne += 1
        Label (self.nbTab1, text = "Adresse :").grid(row = vLigne, column = 0, sticky = W)
        self.eAdr = Entry(self.nbTab1)
        self.eAdr.grid(row = vLigne, column = 1, columnspan = 6, sticky = W+E)
        vLigne += 1

        # Détresse
        Label (self.nbTab1, text = "Nature de la Détresse", fg = "blue",bg = "darkgrey").grid(row = vLigne, column = 0,columnspan = 9, sticky = W+E)
        vLigne += 1
        Label (self.nbTab1, text = "Nature : ").grid(row = vLigne, column = 0, sticky = W)
        self.cbNature = Commun.comboWidget (self.root, self.nbTab1, self.root.cfgListe['Nature'])
        self.cbNature.grid(row = vLigne, column = 1, columnspan = 2, sticky = W)
        Label (self.nbTab1, text = "Détresse Vitale : ").grid(row = vLigne, column = 3, sticky = W)
        self.cbVitale = Commun.comboWidget (self.root, self.nbTab1, self.root.cfgListe['Detresse'])
        self.cbVitale.grid(row = vLigne, column = 4, columnspan = 2, sticky = W)
        Label (self.nbTab1, text = "Tri PMA : ").grid(row = vLigne, column = 6, sticky = W)
        self.cbUrgence = Commun.comboWidget (self.root, self.nbTab1, self.root.cfgListe['Urgence'])
        self.cbUrgence.grid(row = vLigne, column = 7, columnspan = 2, sticky = W)
        vLigne += 1
        Label (self.nbTab1, text = "Circonstances :" ).grid( row = vLigne, column = 0, sticky = W)
        self.stCirc = ScrolledText (self.nbTab1, wrap="word", height = 3)
        self.stCirc.grid(row = vLigne, column = 1, columnspan = 6, sticky = W+E)
        vLigne += 1

        self.nbTab2 = self.notebook.add('Bilan Vital')
        # Conscience
        self.fConsc = LabelFrame(self.nbTab2, bd = 2)
        self.fConsc.grid(row = vLigne, column = 0, columnspan = 3, sticky = N+S)
        Label (self.fConsc, text = "Conscience", fg = "blue",bg = "darkgrey").grid(row = vLigne, column = 0,columnspan = 3, sticky = W+E)
        self.rbConsc = Pmw.RadioSelect(self.fConsc, buttontype = "radiobutton", labelpos = W, label_text = "Victime :", pady = 0)
        self.rbConsc.grid(row = vLigne+1, column = 0, columnspan = 2,sticky = W)
        self.rbConsc.add("Consciente")
        self.rbConsc.add("Inconsciente")
        self.rsConsc = Pmw.RadioSelect(self.fConsc, buttontype = 'checkbutton')
        self.rsConsc.grid(row = vLigne+2, column = 0, columnspan = 3, sticky = W+E)
        for txt in ("Agitée", "Somnolente", "Désorientée", "Nausée"): self.rsConsc.add(txt)
        self.iPCI = IntVar()
        self.ckPCI = Checkbutton (self.fConsc, text = "PCI :", variable = self.iPCI, command = self.cocherPCI)
        self.ckPCI.grid(row = vLigne+3, column = 0, sticky = E)
        self.eTmpPci = Entry(self.fConsc)
        self.eTmpPci.grid(row = vLigne+3, column = 1, sticky = W)

        # Ventilation 
        self.fVentil = LabelFrame(self.nbTab2, bd = 2)
        self.fVentil.grid(row = vLigne, column = 3, columnspan = 3, sticky = N+S)
        Label (self.fVentil, text = "Ventilation", fg = "blue", bg = "darkgrey").grid(row = vLigne, column = 3,columnspan = 3, sticky = W+E)
        Label (self.fVentil, text = "Fréquence :" ).grid(row = vLigne+1, column = 3, pady = 2, sticky = W)
        self.efFreqVent = Pmw.EntryField(self.fVentil, validate = Commun.nonVideValidator)
        self.efFreqVent.grid(row = vLigne+1, column = 4, sticky = W)
        self.rsVentil = Pmw.RadioSelect(self.fVentil, buttontype = 'checkbutton')
        self.rsVentil.grid(row = vLigne+2, column = 3, columnspan = 3, sticky = W+E)
        for txt in ("Ample", "Régulière", "Cyanose", "Sueurs"): self.rsVentil.add(txt)
        Label (self.fVentil, text = "Saturation :" ).grid( row = vLigne+3, column = 3, pady = 1, sticky = W ) 
        self.eSat02 = Entry(self.fVentil)
        self.eSat02.grid(row = vLigne+3, column = 4, sticky = W)
        
        # Circulation 
        self.fCircul = LabelFrame(self.nbTab2, bd = 2)
        self.fCircul.grid(row = vLigne, column = 6, columnspan = 3, sticky = N+S)
        Label (self.fCircul, text = "Circulation", fg = "blue", bg = "darkgrey").grid(row = vLigne, column = 6,columnspan = 3, sticky = W+E)
        Label (self.fCircul, text = "Fréquence :" ).grid(row = vLigne+1, column = 6, pady = 2, sticky = W)
        self.efFreqCirc = Pmw.EntryField(self.fCircul, validate = Commun.nonVideValidator)
        self.efFreqCirc.grid(row = vLigne+1, column = 7, sticky = W)
        self.rsCircul = Pmw.RadioSelect(self.fCircul, buttontype = 'checkbutton')
        self.rsCircul.grid(row = vLigne+2, column = 6, columnspan = 3, sticky = W+E)
        for txt in ("Régulier", "Frappé", "Pâleur", "Pouls radial"): self.rsCircul.add(txt)
        Label (self.fCircul, text = "Tension :" ).grid( row = vLigne+3, column = 6, pady = 1, sticky = W ) 
        self.eTension = Entry(self.fCircul)
        self.eTension.grid(row = vLigne+3, column = 7, sticky = W)
        vLigne += 4
        
        # Pupilles
        Label (self.nbTab2, text = "Réflexes Pupillaires", fg = "blue",bg = "darkgrey").grid(row = vLigne, column = 0,columnspan = 9, sticky = W+E)
        vLigne += 1
        Label (self.nbTab2, text = "Pupille Gauche :").grid(row = vLigne, column = 0, sticky = W)
        self.cbPupGauche = Commun.comboWidget(self.root, self.nbTab2, self.root.cfgListe['pupille'])
        self.cbPupGauche.grid(row = vLigne, column = 1, sticky = W)
        self.iPupGauche = IntVar()
        self.ckPupGauche = Checkbutton (self.nbTab2, text = "Réactive", variable = self.iPupGauche)
        self.ckPupGauche.grid(row = vLigne, column = 2, sticky = W)
        Label (self.nbTab2, text = "Pupille Droite :").grid(row = vLigne, column = 4, sticky = W)
        self.cbPupDroite = Commun.comboWidget(self.root, self.nbTab2, self.root.cfgListe['pupille'])
        self.cbPupDroite.grid(row = vLigne, column = 5, sticky = W)
        self.iPupDroite = IntVar()
        self.ckPupDroite = Checkbutton (self.nbTab2, text = "Réactive", variable = self.iPupDroite)
        self.ckPupDroite.grid(row = vLigne, column = 6, sticky = W)
        vLigne += 1

        self.nbTab3 = self.notebook.add('Bilan Lésionnel')
        self.nbTab3.grid_columnconfigure(0, weight=2)
        self.nbTab3.grid_columnconfigure(10, weight=2)
        # Lésions  
        Label (self.nbTab3, text = "Lésions", fg = "blue",bg = "darkgrey").grid(row = vLigne, column = 0, columnspan = 11, sticky = W+E)
        vLigne += 1

        vLibLesion = ["Hémorragie ","Déformation","  Douleur  ","   Plaie   ","  Brûlure  "," Motricité ","Sensibilité","  Chaleur  ","Coloration"]
        for index in range(9):
            Label (self.nbTab3, text = vLibLesion[index]).grid(row = vLigne, column = index+1, sticky = W+E)
        vLigne += 1
        
        for i in range (5):
            cbLesion = Commun.comboWidget(self.root, self.nbTab3, self.root.cfgListe['Lesion'])
            cbLesion.grid(row = vLigne, column = 0, sticky = E)
            vCodLesion = ["H","F","D","P","B","M","S","C","K"]
            self.listeCkLesion = []
            for index in range(9):
                iCk = IntVar()
                ck = Checkbutton (self.nbTab3, text = vCodLesion[index]+str(i), variable = iCk, width=8)
                ck.grid(row = vLigne, column = index+1)
                self.listeCkLesion.append(iCk) 
            vLigne += 1
            self.ligneLesion.append((cbLesion,self.listeCkLesion))

        Label (self.nbTab3, text = "Autres lésions").grid(row = vLigne, column = 1, sticky = W)
        self.eAutreLes = Entry(self.nbTab3)
        self.eAutreLes.grid(row = vLigne, column = 2, columnspan = 7, sticky = W+E)
        vLigne += 1

        self.nbTab4 = self.notebook.add('Gestes et Soins')
        self.nbTab4.grid_columnconfigure(0, weight=2)  
        self.nbTab4.grid_columnconfigure(2, weight=1)
        self.nbTab4.grid_columnconfigure(3, weight=2)
        self.nbTab4.grid_columnconfigure(5, weight=1)
        self.nbTab4.grid_columnconfigure(6, weight=2)
        self.nbTab4.grid_columnconfigure(8, weight=1)
        # Antécédants
        Label (self.nbTab4, text = "Gestes et Soins", fg = "blue",bg = "darkgrey").grid(row = vLigne, column = 0,columnspan = 9, sticky = W+E)
        vLigne += 1
        Label (self.nbTab4, text = "Gestes effectués :" ).grid(row = vLigne, column = 0, sticky = W)
        self.stGestes = ScrolledText (self.nbTab4, wrap="word", height = 3)
        self.stGestes.grid(row = vLigne, column = 1, columnspan = 6, sticky = W+E)
        vLigne += 1
        Label (self.nbTab4, text = "Soins effectués :" ).grid( row = vLigne, column = 0, sticky = W)
        self.stSoins = ScrolledText (self.nbTab4, wrap="word", height = 3)
        self.stSoins.grid(row = vLigne, column = 1, columnspan = 6, sticky = W+E)
        vLigne += 1
        # Evacuation
        Label (self.nbTab4, text = "Evacuation", fg = "blue",bg = "darkgrey").grid(row = vLigne, column = 0,columnspan = 9, sticky = W+E)
        vLigne += 1
        Label (self.nbTab4, text = "Prise en Charge :").grid(row = vLigne, column = 0, sticky = W)
        self.cbCondi = Pmw.ComboBox (self.nbTab4, scrolledlist_items = self.root.cfgListe['conditionnement'], listheight = 80 )
        self.cbCondi.grid (row = vLigne, column = 1, sticky = W)
        Label (self.nbTab4, text = "Evacuation :").grid(row = vLigne, column = 3, sticky = W)
        self.cbEvac = Pmw.ComboBox (self.nbTab4, scrolledlist_items = self.root.cfgListe['evacuation'], listheight = 80 )
        self.cbEvac.grid (row = vLigne, column = 4, sticky = W)
        Label (self.nbTab4, text = "Destination : " ).grid( row = vLigne, column = 6, sticky = W )
        self.eDest = Entry(self.nbTab4)
        self.eDest.grid (row = vLigne, column = 7)
        vLigne += 1

        self.notebook.setnaturalsize()
        Label (vFen,text="Final du message ", fg="blue",bg="cyan").grid(row=vLigne, column=0, columnspan=9, sticky=E+W)
        vLigne += 1
        Label (vFen, text="GDH Dépôt/Rédaction : ").grid(row=vLigne, column=0, sticky=W )
        self.efGdhDep = Commun.gdhWidget(vFen, vFen)
        self.efGdhDep.grid (row=vLigne, column=1, sticky=W)
        self.rbACK = Pmw.RadioSelect(vFen, buttontype="radiobutton",labelpos=W,label_text="Demande Accusé de Réception : ")
        self.rbACK.grid(row=vLigne, column=3, columnspan=3, sticky=W)
        self.rbACK.add("Oui")
        self.rbACK.add("Non")
        vLigne += 1
      
        Label (vFen,text = "Fin de Message", fg = "blue",bg = "orange").grid(row = vLigne, column = 0, columnspan = 9, sticky = E+W)
        vLigne += 1

        Button (vFen, text = "Valider", command = self.validerBILSEC, fg = "red", underline = 0).grid(row = vLigne, column = 1, padx = 5, pady = 5, sticky = W+E)
        Button (vFen, text = "Annuler", command = self.annulerBILSEC, fg = "red", underline = 1).grid(row = vLigne, column = 4, padx = 5, pady = 5, sticky = W+E)
        Button (vFen, text = "Quitter", command = self.quitterBILSEC, fg = "red", underline = 0).grid(row = vLigne, column = 7, padx = 5, pady = 5, sticky = W+E)


    # Définition des bulles d'aide sur la fenêtre
    def bulleAide(self):
        # ATTENTION, les message d'aide des Widgets GesADRA sont déjà gérés
        self.fenetre.bulle.bind(self.efNum, "Nombre de 1 à 5 chiffres ou 'Auto'")
        self.fenetre.bulle.bind(self.stCirc, "Texte sur plusieurs lignes si besoin")
        self.fenetre.bulle.bind(self.stGestes, "Texte sur plusieurs lignes si besoin")
        self.fenetre.bulle.bind(self.stSoins, "Texte sur plusieurs lignes si besoin")
        
    # Action sur un bouton "Auto"
    def numAuto(self, evt = None):
        self.efNum.setvalue('Auto')
        

    def validerBILSEC(self, evt = None):
        "Traitement du bouton 'Valider'"

        #Contrôle de la validité des données
        if self.controleSaisie() == False:
            # Si erreur, on stoppe le traitement
            return None

        # Recalcul des données variables (Gdh, N° message, etc...)
        if self.iGdh.get() == True :
            self.efGdh.setvalue("")
            vGdh = datetime.datetime.now().strftime("%d/%m/%y %H:%M")
            self.efGdh.setvalue(vGdh)
            
        # Rédaction du message
        self.redigerBILSEC()
        
        # Impression
        if self.root.userData['IMPR_MSG'] == "OUI" :
            os.startfile(Commun.getFullPath(self.root, self.vFicBILSEC+".TXT"))
            tkMessageBox.showinfo('Bilan Secouriste', 'Lancez une impression manuelle au format "Paysage" SVP')
        else :
            tkMessageBox.showinfo('Bilan Secouriste', 'Message créé : ' + self.vFicBILSEC)
        #self.fenetre.destroy()


    def annulerBILSEC(self, evt = None):
        "Traitement du bouton 'Annuler'"
        self.razSaisie()


    def quitterBILSEC(self, evt = None):
        "Traitement du bouton 'Quitter'"
        etesVousSur = tkMessageBox.askquestion("Fermeture du Formulaire", \
                                               "Confirmez-vous la fermeture du Bilan Secouriste ?")
        if etesVousSur == "yes" :
            self.fenetre.destroy()
        else:
            self.fenetre.focus_set()


    def razSaisie(self):

        vGdh = datetime.datetime.now().strftime("%d/%m/%y %H:%M")
        self.efGdh.setvalue(vGdh) # Gdh transmission
        self.ckGdh.select() # Cocher pour recalculer le Gdh
        self.cbEmetteur.setentry("")
        self.cbDestinataire.setentry("")
        self.eInstruc.delete(0,END)
        self.efOrigine.setvalue("")
        self.efDestAction.setvalue("")
        self.eDestInfo.delete(0,END)
        self.cbDegUrg.selectitem(self.root.userData['URG_BILSEC'])
        self.efNum.setvalue("")
        self.eAge.delete(0,END)
        self.rbSexe.selection = None
        self.eNom.delete(0,END)
        self.eAdr.delete(0,END)
        self.cbNature.setentry("")
        self.cbVitale.setentry("")
        self.cbUrgence.setentry("")
        self.stCirc.delete(1.0,END)
        self.rbConsc.selection = None
        self.rsConsc.setvalue(["","","",""])
        self.iPCI.set(False)
        self.cocherPCI() 
        self.efFreqVent.setvalue("")
        self.rsVentil.setvalue(["","","",""])
        self.eSat02.delete(0,END)
        self.efFreqCirc.setvalue("")
        self.rsCircul.setvalue(["","","",""])
        self.eTension.delete(0,END)
        self.cbPupGauche.setentry("")
        self.iPupGauche.set(False)
        self.cbPupDroite.setentry("")
        self.iPupDroite.set(False)
        for ligne in self.ligneLesion : 
            self.initLesion(ligne[0])
            for choix in ligne[1]:
                choix.set(False)
        self.eAutreLes.delete(0,END)
        self.stGestes.delete(1.0,END)
        self.stSoins.delete(1.0,END)
        self.cbCondi.setentry("")
        self.cbEvac.setentry("")
        self.eDest.delete(0,END)
        self.efGdhDep.setvalue(vGdh)
        self.rbACK.invoke("Non")


    def controleSaisie(self):
        if not (self.efGdh.valid() and self.cbEmetteur.valid() and self.cbDestinataire.valid()):
            tkMessageBox.showwarning('Contrôle', 'Les champs en rouge sont absents ou incorrects')
            self.fenetre.focus_set()
            return False
        if not self.efNum.valid():
            tkMessageBox.showwarning('Contrôle', 'Numéro de victime incorrect')
            self.notebook.selectpage(0)
            self.efNum.focus_set()
            return False
        else:
            if self.efNum.getvalue() == 'Auto':
                self.efNum.setvalue(Commun.getNumVict(self.root))
            else:   
                self.efNum.setvalue(self.efNum.getvalue().zfill(5))
        if self.rbSexe.getvalue() == None:
            tkMessageBox.showwarning('Contrôle', 'Indiquez le sexe de la victime')
            self.notebook.selectpage(0)
            self.rbSexe.component("H").focus_set()
            return False
        if not (self.efFreqVent.valid() and self.efFreqCirc.valid()):
            tkMessageBox.showwarning('Contrôle', 'Les champs en rouge sont absents ou incorrects')
            self.notebook.selectpage(1)
            self.fenetre.focus_set()
            return False
        if self.rbConsc.getvalue() == None:
            tkMessageBox.showwarning('Contrôle', 'Préciez l\'état de conscience')
            self.notebook.selectpage(1)
            self.rbConsc.component("Consciente").focus_set()
            return False
        
        return True 
            

    def cocherPCI(self):
        # Autoriser la saisie de la durée PCI
        if self.iPCI.get() == True:
            self.eTmpPci.configure(state = NORMAL)
            self.eTmpPci.insert(0,u"Durée PCI : ")
            self.eTmpPci.focus_set()            
        else:
            self.eTmpPci.delete(0,END)
            self.eTmpPci.configure(disabledbackground = "lightgray", state = DISABLED)

    # Traitement du bind <Return> spécifique
    def notReturn1 (self, evt = None):
        """Reproduire le comportement normal de la touche <Entrée> pour un ScrolledText"""
        self.stCirc.insert(self.stCirc.index(INSERT), "\n")
        return "break"
    # Traitement du bind <Return> spécifique
    def notReturn2 (self, evt = None):
        """Reproduire le comportement normal de la touche <Entrée> pour un ScrolledText"""
        self.stGestes.insert(self.stGestes.index(INSERT), "\n")
        return "break"
    # Traitement du bind <Return> spécifique
    def notReturn3 (self, evt = None):
        """Reproduire le comportement normal de la touche <Entrée> pour un ScrolledText"""
        self.stSoins.insert(self.stSoins.index(INSERT), "\n")
        return "break"

    def initLesion(self, cbLesion):
        # Raz de cbLesion (combo sans saisie)
        cbLesion.component('entryfield_entry').configure(state = NORMAL)
        cbLesion.setentry("")
        cbLesion.component('entryfield_entry').configure(state = DISABLED, disabledforeground = 'black', disabledbackground = 'white')
        
    
    # Creation des fichiers message
    def redigerBILSEC(self):

        # Nom du fichier
        self.vFicBILSEC = Commun.getFicBILSEC(self.root)
        # Fichier TXT
        self.txtFileBILSEC()
        # Fichier XML
        self.xmlFileBILSEC()
        
        
        # Ecriture d'une ligne dans la main courante
        vTexte = "Message " + self.vFicBILSEC + \
		         " de " + self.efOrigine.getvalue() + " vers " +  self.efDestAction.getvalue()
        infosMCI = Commun.InfosMCI(self.efGdh.getvalue(), self.cbEmetteur.get(), self.cbDestinataire.get(), \
                                   self.cbDegUrg.get(), " ", vTexte)
        infosMCI.ecrire(self.root)
        
    
    def txtFileBILSEC(self):
        
        fic = open(Commun.getFullPath(self.root, self.vFicBILSEC+".TXT"), 'w')
        
        fic.write(self.vFicBILSEC+"\n\n")
        fic.write('################################################################################\n')
        fic.write('- '+(self.root.userData['ACTIVATION'] + ' - ')*3+'\n')
        fic.write('--------------------------------------------------------------------------------\n')
    
        # Informations transmission
        fic.write("GDH Emission : " + self.efGdh.getvalue()+ "\n")
        fic.write("Emis par     : " + self.cbEmetteur.get()+ "\n")
        fic.write("Reçu par     : " + self.cbDestinataire.get()+ "\n")
        fic.write("Instructions : " + self.eInstruc.get()+ "\n")
        fic.write('================================================================================\n')

        # Entête du message
        fic.write("BILAN SECOURISTE".center(80) + "\n")
        fic.write("Origine      : " + self.efOrigine.getvalue()+"\n")
        fic.write("Dest. Action : " + self.efDestAction.getvalue()+"\n")
        fic.write("Dest. Info   : " + self.eDestInfo.get()+"\n")
        fic.write("Urgence      : " + self.cbDegUrg.get()+"\n")
        fic.write('--------------------------------------------------------------------------------\n')

        # Corps du message
        fic.write("------Identité de la Victime-------\n")
        fic.write("Num Victime  : " + self.efNum.getvalue() +"\n")
        fic.write("Age          : " + self.eAge.get() +"\n")
        fic.write("Sexe         : " + self.rbSexe.getvalue() +"\n")
        fic.write("Nom - Prénom : " + self.eNom.get() +"\n")
        fic.write("Adresse : " + self.eAdr.get() +"\n")

        fic.write("------Nature de la detresse--------\n")
        fic.write("Nature        : " + self.cbNature.get() +"\n")
        fic.write("Détr. Vitale  : " + self.cbVitale.get() +"\n")
        fic.write("Tri PMA       : " + self.cbUrgence.get() +"\n")
        fic.write("Circonstances :\n")
        # découpage des lignes du message
        for ligne in self.stCirc.get(1.0,END).split("\n"):
            if len(ligne) > 79:
                for ligne in textwrap.wrap(ligne,79):
                    fic.write(ligne +"\n")
            else:
               fic.write(ligne + "\n")

        # Conscience
        fic.write('--------------Conscience--------------\n')
        fic.write("Victime      : " + self.rbConsc.getvalue() + " ")
        for item in self.rsConsc.getvalue():
            if item.strip != "": fic.write(item.strip() + " ")
        fic.write("\n")    
        fic.write("PCI          : ")
        if self.iPCI.get() == True:
            fic.write("OUI " + self.eTmpPci.get()+"\n")
        else:
            fic.write("NON\n")

        fic.write('--------------Ventilation--------------\n')
        fic.write("Fréquence    : " + self.efFreqVent.getvalue() + " ")
        for item in self.rsVentil.getvalue():
            if item.strip != "": fic.write(item.strip() + " ")
        fic.write("\n")    
        fic.write("Saturation   : " + self.eSat02.get() + "\n")

        fic.write('--------------Circulation--------------\n')
        fic.write("Fréquence    : " + self.efFreqCirc.getvalue() + " ")
        for item in self.rsCircul.getvalue():
            if item.strip != "": fic.write(item.strip() + " ")
        fic.write("\n")    
        fic.write("Tension      : " + self.eTension.get()+"\n")

        fic.write("---------Réflexes Pupillaires----------\n")
        fic.write("Pup. Gauche  : "+ self.cbPupGauche.get())
        if self.iPupGauche.get() == True: fic.write(" Réactive")
        fic.write ("\n")   
        fic.write("Pup. Droite  : "+ self.cbPupDroite.get())
        if self.iPupDroite.get() == True: fic.write(" Réactive")
        fic.write ("\n")   

        fic.write("----------------Lésions----------------\n")
        fic.write("                  Hémorragie Déformation  Douleur     Plaie     Brulure   Motricité Sensibilité  Chaleur  Coloration \n")
        for ligne in self.ligneLesion : 
            try:
                fic.write (ligne[0].get().center(18))
                for choix in ligne[1]:
                    if choix.get() == True:
                       fic.write ("X".center(11))
                    else:
                       fic.write (" ".center(11))
                fic.write("\n")
            except:
                None
        fic.write("Autres      : " + self.eAutreLes.get()+"\n")

        fic.write("----------------Gestes-----------------\n")
        for ligne in self.stGestes.get(1.0,END).split("\n"):
            if len(ligne) > 79:
                for ligne in textwrap.wrap(ligne,79):
                    fic.write(ligne +"\n")
            else:
               fic.write(ligne + "\n")

        fic.write("-----------------Soins-----------------\n")
        for ligne in self.stSoins.get(1.0,END).split("\n"):
            if len(ligne) > 79:
                for ligne in textwrap.wrap(ligne,79):
                    fic.write(ligne +"\n")
            else:
               fic.write(ligne + "\n")

        fic.write('------------Evacuation------------\n')
        fic.write("Conditionné  : " + self.cbCondi.get() + "\n")
        fic.write("Evacutation  : " + self.cbEvac.get() + "\n")
        fic.write("Orientation  : " + self.eDest.get()+"\n")

        fic.write("\n")
        fic.write("FIN DE MESSAGE".center(80) + "\n")
        fic.write('================================================================================\n')
        fic.write('- ' +(self.root.userData['ACTIVATION'] + ' - ')*3+'\n')
        fic.write('################################################################################\n')

        fic.close()

    #
    def xmlFileBILSEC(self):

        fic = open(Commun.getFullPath(self.root, self.vFicBILSEC+".XML"),'w')
        
        fic.write('<?xml version="1.0" encoding="iso-8859-15"?><?xml-stylesheet type="text/xsl" href="..\msgBILSEC.XSL"?>\n')
        fic.write('<msg>\n')
        fic.write('<form>Message BILSEC</form>\n')
        fic.write('<soft>' + self.root.userData['LOGICIEL'] + '</soft>\n')
        fic.write('<vers>' + self.root.userData['VERSION'] + '</vers>\n')
        fic.write('<mode>' + self.root.userData['ACTIVATION'] + '</mode>\n')
        fic.write('<trans>\n')
        fic.write('<gdh>' + self.efGdh.getvalue()+'</gdh>\n')
        fic.write('<emis>' + self.cbEmetteur.get()+'</emis>\n')
        fic.write('<recu>' + self.cbDestinataire.get()+"</recu>\n")
        fic.write("<instr>" + self.eInstruc.get()+"</instr>\n")
        fic.write('</trans>\n')
        fic.write("<top>\n")
        fic.write("<from>" + self.efOrigine.getvalue()+"</from>\n")
        fic.write("<to>" + self.efDestAction.getvalue()+"</to>\n")
        fic.write("<info>" + self.eDestInfo.get()+"</info>\n")
        fic.write("<urg>" + self.cbDegUrg.get()+"</urg>\n")
        fic.write('</top>\n')
        fic.write("<corps>\n")
        fic.write("<ong1>\n")
        fic.write("<num>" + self.efNum.getvalue()+"</num>\n")
        fic.write("<age>" + self.eAge.get() +"</age>\n")
        fic.write("<sexe>" + self.rbSexe.getvalue() +"</sexe>\n")
        fic.write("<nom>" + self.eNom.get() +"</nom>\n")
        fic.write("<adr>" + self.eAdr.get() +"</adr>\n")
        fic.write("<nat>" + self.cbNature.get() +"</nat>\n")
        fic.write("<vital>" + self.cbVitale.get() +"</vital>\n")
        fic.write("<pma>" + self.cbUrgence.get() +"</pma>\n")
        # découpage des lignes du message
        for ligne in self.stCirc.get(1.0,END).split("\n"):
            if len(ligne) > 79:
                for ligne in textwrap.wrap(ligne,79):
                    fic.write("<circ>" + ligne +"</circ>\n")
            else:
                fic.write("<circ>" + ligne +"</circ>\n")
        fic.write("</ong1>\n")
        fic.write("<ong2>\n")
        fic.write("<consc>\n")
        fic.write("<etat>" + self.rbConsc.getvalue() + "</etat>\n")
        for item in self.rsConsc.getvalue(): 
            if item.strip() != "": fic.write("<item>" + item.strip() + "</item>\n")    
        if self.iPCI.get() == True:
            fic.write("<pci>OUI " + self.eTmpPci.get()+"</pci>\n")
        else:
            fic.write("<pci>NON</pci>\n")
        fic.write("</consc>\n")    
        fic.write("<ventil>\n")
        fic.write("<freq>" + self.efFreqVent.getvalue() + "</freq>\n")
        for item in self.rsVentil.getvalue():
            if item.strip() != "": fic.write("<item>" + item.strip() + "</item>\n")
        fic.write("<sat>" + self.eSat02.get() + "</sat>\n")
        fic.write("</ventil>\n")    
        fic.write('<circul>\n')
        fic.write("<freq>" + self.efFreqCirc.getvalue() + "</freq>\n")
        for item in self.rsCircul.getvalue(): 
            if item.strip() != "": fic.write("<item>" + item.strip() + "</item>\n")
        fic.write("<tension>" + self.eTension.get()+"</tension>\n")
        fic.write("</circul>\n")    
        fic.write("<pupil>\n")
        fic.write("<gauche>" + self.cbPupGauche.get() + "</gauche>\n")
        fic.write("<reacg>" + str(self.iPupGauche.get()) + "</reacg>\n")
        fic.write("<droite>" + self.cbPupDroite.get() + "</droite>\n")
        fic.write("<reacd>" + str(self.iPupDroite.get()) + "</reacd>\n")
        fic.write ("</pupil>\n")   
        fic.write("</ong2>\n")
        fic.write("<ong3>\n")
        for ligne in self.ligneLesion : 
            if ligne[0].get().strip() != "":
                fic.write ("<lesion>\n")
                fic.write ("<zone>" + ligne[0].get() + "</zone>\n")
                for choix in ligne[1]: 
                    fic.write("<val>")
                    if choix.get() == True: fic.write ("X")
                    fic.write("</val>\n")
                fic.write("</lesion>\n")
        fic.write("<autreles>" + self.eAutreLes.get()+"</autreles>\n")
        fic.write("</ong3>\n")
        fic.write("<ong4>\n")
        for ligne in self.stGestes.get(1.0,END).split("\n"):
            if len(ligne) > 79:
                for ligne in textwrap.wrap(ligne,79):
                    fic.write("<geste>" + ligne +"</geste>\n")
            else:
               fic.write("<geste>" + ligne + "</geste>\n")
        for ligne in self.stSoins.get(1.0,END).split("\n"):
            if len(ligne) > 79:
                for ligne in textwrap.wrap(ligne,79):
                    fic.write("<soin>" + ligne +"</soin>\n")
            else:
               fic.write("<soin>" + ligne + "</soin>\n")
        fic.write("<condi>" + self.cbCondi.get() + "</condi>\n")
        fic.write("<evac>" + self.cbEvac.get() + "</evac>\n")
        fic.write("<dest>" + self.eDest.get()+"</dest>\n")
        fic.write("</ong4>\n")
        fic.write('</corps>\n')
        fic.write('<bot>\n')
        fic.write("<gdh>" + self.efGdhDep.getvalue()+"</gdh>\n")
        fic.write("<ack>" + self.rbACK.getvalue()+"</ack>\n")
        fic.write('</bot>\n')
            
        fic.write('</msg>\n')
    
        fic.close()
    #
