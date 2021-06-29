# -*- coding: iso-8859-15 -*-

from tkinter import *
from tkinter.scrolledtext import ScrolledText

import datetime
import time
import os
import tkinter.messagebox as tkMessageBox
import tkinter.simpledialog as tkSimpleDialog
import Pmw
import sys
import Commun # Module principal des fonctions annexes

###################### Gestion des relevés Sater.
class FormGSat:
    """Classe définissant le formulaire Relevé Sater"""
    
    def __init__(self, appli):
        """Constructeur de l'onglet Sater"""
        self.root = appli # Référence à l'application racine
        self.fenetre = self.root.notebook.add('Log. Relevés Sater')
        self.boutonE = [] # liste des boutons EMETTEUR

        # Composants de la fenêtre
        self.drawGSat()
        self.razSaisie()

        # Alimentation de la liste
        self.alimListe()        

        # Gestion des raccourcis clavier
        self.selectTab()
     

    def drawGSat(self):

        # variables locales
        vLigne = 1 # N° de ligne pour le positionnement des composants
        vFen = self.fenetre

        # Le label zone cachée "réserve" la place du bouton[0] dans le gridder
        #Label (vFen,text = "zone cachée", bg = "orange",width=9).grid(row = vLigne, column = 1, sticky = E+W)
        Label (vFen,text = "Stations présentes sur le réseau", fg = "blue",bg = "orange").grid(row = vLigne, column = 0,columnspan = 16, sticky = E+W)
        vLigne += 1
        
        # 14 boutons "Emetteur"
        Label (vFen, text = "Reçu de :").grid(row = vLigne, column = 0)
        for indice in range(0, 15):
            bouton = Button(vFen, foreground = "red", takefocus = 1) # width=8
            bouton.grid(column = indice, row = vLigne, sticky = E+W)
            bouton.configure(command = lambda x = indice : self.cliquerRecuDe(x))
            if indice == 0: bouton.grid_remove() # Suppression du bouton 0 "Tous"  
            self.boutonE.append(bouton)
        vLigne += 1
        
        # Données du relevé
        Label (vFen,text = "Informations Relevé Sater ", fg = "blue",bg = "orange").grid(row = vLigne, column = 0, columnspan = 16, sticky = E+W)
        vLigne += 1
        
        Label (vFen, text = "Groupe Date/Heure : ").grid(row = vLigne, column = 0, sticky = W)
        self.efGdh = Commun.gdhWidget(self.root, vFen)
        self.efGdh.grid(row = vLigne, column = 1, columnspan = 2, sticky = W)
        self.bGdh = Button(self.fenetre, bd = 1, fg = "blue", text = "Forcer", command = self.forcerGDH, underline = 0) # , width = 8
        self.bGdh.grid(row = vLigne, column = 3)
        vLigne += 1
        
        Label (vFen, text = "Emis par : ").grid(row = vLigne, column = 0, sticky = W)
        self.cbEmetteur = Commun.indicatifWidget(self.root, vFen, self.root)
        self.cbEmetteur.grid (row = vLigne, column = 1, columnspan = 3, sticky = W)
        Label (vFen, text = "Reçu par : ").grid(row = vLigne, column = 4, columnspan = 2, sticky = W)
        self.cbDestinataire = Commun.indicatifWidget(self.root, vFen, self.root)
        self.cbDestinataire.grid (row = vLigne, column = 6, columnspan = 3, sticky = W)
        vLigne += 2
         
        Label (vFen, text = "Système : ").grid(row = vLigne, column = 0, sticky = W)
        self.cbSysteme = Commun.comboWidget (self.root, vFen, self.root.cfgListe['Systeme'])
        self.cbSysteme.grid (row = vLigne, column = 1, columnspan = 3, sticky = W)
        Label (vFen, text = "Datum : ").grid(row = vLigne, column = 4, columnspan = 2, sticky = W)
        self.cbDatum = Commun.comboWidget (self.root, vFen, self.root.cfgListe['Datum'])
        self.cbDatum.grid (row = vLigne, column = 6, columnspan = 3, sticky = W)
        vLigne += 1
        
        Label (vFen, text = "Coordonnée X :").grid(row = vLigne, column = 0, sticky = W)
        self.efCoordX = Commun.coordWidget(self.root, vFen)
        self.efCoordX.grid (row = vLigne, column = 1, columnspan = 2, sticky = W)
        Label (vFen, text = "Coordonnée Y :").grid(row = vLigne, column = 4, columnspan = 2, sticky = W)
        self.efCoordY = Commun.coordWidget(self.root, vFen)
        self.efCoordY.grid (row = vLigne, column = 6, columnspan = 2, sticky = W)
        vLigne += 1

        Label (vFen, text = "Direction du relevé :").grid(row = vLigne, column = 0, sticky = W)
        self.efDir = Pmw.EntryField (vFen, validate = {"max" : 5, "maxstrict" : False, "validator" : Commun.nonVideValidator})
        self.efDir.grid(row = vLigne, column = 1, columnspan = 2, sticky = W)
        Label (vFen, text = "Force du signal :").grid(row = vLigne, column = 4, columnspan = 2, sticky = W)
        self.efForce = Pmw.EntryField (vFen, validate = {"max" : 5, "maxstrict" : False})
        self.efForce.grid(row = vLigne, column = 6, columnspan = 2, sticky = W)
        vLigne += 1

        Label (vFen, text = "Commentaire : " ).grid( row = vLigne, column = 0, sticky = W )
        self.efComment = Pmw.EntryField(vFen, validate = {"max" : 80, "maxstrict" : False})
        self.efComment.grid(row = vLigne, column = 1, columnspan = 8, sticky = E+W )
        vLigne += 1
        
        self.bValider = Button (vFen, text = "Valider", command = self.validerGSat, fg = "red", underline = 0)
        self.bValider.grid (row = vLigne, column = 2, columnspan = 2, sticky = E+W, padx = 5,pady = 5 )
        self.bEffacer = Button (vFen, text = "Effacer", command = self.effacerGSat, fg = "red", underline = 0)
        self.bEffacer.grid (row = vLigne, column = 4, columnspan = 2, sticky = E+W, padx = 5,pady = 5)
        self.bQuitter = Button (vFen, text = "Quitter", command = self.quitterGSat, fg = "red", underline = 0)
        self.bQuitter.grid (row = vLigne, column = 7, columnspan = 2, sticky = E+W, padx = 5,pady = 5)
        vLigne += 1

        # Dernières infos de la vacation
        Label (vFen,text = "Derniers relevés enregistrés", fg = "blue",bg = "orange").grid( row = vLigne, column = 0, columnspan = 16, sticky = E+W)
        vLigne += 1
        fLog = Frame(vFen)
        fLog.grid(row = vLigne, column = 0, columnspan = 16)
        sbListe = Scrollbar(fLog, orient = VERTICAL)
        self.lbListe = Listbox(fLog, height = 15, width = 140, font = self.root.fonteFixe, yscrollcommand = sbListe.set)
        self.lbListe.grid(row = vLigne, column = 0, sticky = E+W)
        sbListe.config(command = self.lbListe.yview)
        sbListe.grid(row = vLigne, column = 1, sticky = N+S)


    def initBoutons(self):
    
        for i in range(1,15):
            indicatif = self.root.netData["STATION"+str(i)]
            vBulle = self.root.netData["OPERATEUR"+str(i)]+"\n("+self.root.netData["STATUT"+str(i)]+")"
            self.boutonE[i].config(text = indicatif)
            self.root.bulle.bind(self.boutonE[i], vBulle.strip())
    #
            
    # Action sur un bouton "Emetteur"
    def cliquerRecuDe(self, indice):
        # Calcul du GDH, insertion des indicatifs et positionnement sur le texte à saisir
        # Contrôle de l'indicatif 
        indicatif = self.controleIndicatif(indice)
        if indicatif != "":
            # Alimentation des données SATER
            self.razSaisie()
            vGdh = datetime.datetime.now().strftime("%d/%m/%y %H:%M")
            self.efGdh.setvalue(vGdh)
            self.cbEmetteur.component('entryfield').setvalue(indicatif)
            self.cbDestinataire.selectitem(self.root.userData['INDICATIF'])
            self.efCoordX.component('entry').focus_set()
        else :
            self.fenetre.focus_set()

            
    # Contrôle de l'indicatif et saisie si absent
    def controleIndicatif (self, indice, message=None):
        # Message par défaut
        if message == None : message = "Nouvel indicatif :"
        # Si l'indicatif n'est pas dans le dictionnaire Réseau, on demande sa saisie
        indicatif = self.root.netData["STATION"+str(indice)]
        if indicatif == "" :
           indicatif = tkSimpleDialog.askstring("Gestion SATER", message)
           # Si pas de saisie, on rend la main
           if indicatif == None: return ""
           # Contrôle par le validateur
           if Commun.indicatif3Validator(indicatif) == Pmw.OK :
               # Saisie correcte
               indicatif = indicatif.upper()
               self.root.netData["STATION"+str(indice)] = indicatif
               self.root.netData["STATUT"+str(indice)] = "Actif"
               vBulle = self.root.netData["OPERATEUR"+str(indice)]+"\n("+self.root.netData["STATUT"+str(indice)]+")"
               self.root.bulle.bind(self.boutonE[indice], vBulle.strip())               
               self.boutonE[indice].config(text = indicatif)
           else :
               # Erreur : relancer le contrôle de l'indicatif (récursivité)
               indicatif = self.controleIndicatif (indice, "Saisie incorrecte : l'indicatif doit être de 2 à 8 car.,\n" +
                                                           "sans accent ni espace (tiret, slash et souligné permis) :")
               
        return indicatif
    

    # Action sur un bouton "Forcer GDH"
    def forcerGDH(self, evt = None):
        vGdh = datetime.datetime.now().strftime("%d/%m/%y %H:%M")
        self.efGdh.setvalue(vGdh)

    # Action sur un bouton "Valider"
    def validerGSat(self, evt = None):
        "Traitement du bouton 'Valider'"

        #Contrôle de la validité des données
        if self.controleSaisie() == False:
            # Si erreur, on stoppe le traitement
            return False

        # Ligne SATER
        infosSATER = Commun.InfosSATER(self.efGdh.getvalue(), self.cbEmetteur.get(), self.cbDestinataire.get(), \
                                       self.cbSysteme.get(), self.cbDatum.get(), self.efCoordX.getvalue(), \
                                       self.efCoordY.getvalue(), self.efDir.getvalue(), self.efForce.getvalue(), \
                                       self.efComment.getvalue())
        infosSATER.ecrire(self.root)

        self.afficherListe(infosSATER)

        # Ligne de MCI
        vTexte = "Releve SATER :  X = " + self.efCoordX.getvalue() + \
                 ", Y = " + self.efCoordY.getvalue() +", Dir = " + self.efDir.getvalue()
        infosMCI = Commun.InfosMCI(self.efGdh.getvalue(), self.cbEmetteur.get(), self.cbDestinataire.get(), \
                                   self.root.userData['URG_SATER'], " ", vTexte)
        infosMCI.ecrire(self.root)
 
        # Remise à Zéro du formulaire
        self.razSaisie()

        
    # Action sur le bouton "Effacer"
    def effacerGSat(self, evt = None):
        """Traitement du bouton 'Effacer'"""
        # Remise à Zéro de la saisie
        self.razSaisie()


    # Action sur le bouton "Effacer"
    def quitterGSat(self, evt = None):
        """Traitement du bouton 'Quitter'"""
        if self.efGdh.getvalue().strip() != "":
            etesVousSur = tkMessageBox.askquestion("Log. Relevés Sater", \
                                                   "Saisie en cours.\nConfirmez-vous la fermeture de cet onglet ?")
        else:
            etesVousSur = "yes"
            
        if etesVousSur == "yes" :
            self.root.printMenu.delete(self.root.printMenu.index("Log. Sater"))
            self.unSelectTab()
            self.root.notebook.delete('Log. Relevés Sater')
            self.root.fenGSat = None 
            self.fenetre.destroy()
        else:
            self.fenetre.focus_set()

    def createTab(self):
        self.root.printMenu.add_command(label="Log. Sater", command=self.imprimerSater)
    #
    
    def selectTab(self):
        self.initBoutons()

        self.root.bind('<Alt-f>', self.forcerGDH)
        self.root.bind('<Alt-v>', self.validerGSat)
        self.root.bind('<Return>', self.validerGSat)
        self.root.bind('<Alt-e>', self.effacerGSat)
        self.root.bind('<Escape>', self.effacerGSat)
        self.root.bind('<Alt-q>', self.quitterGSat)
    #
        
    def unSelectTab(self):

        self.root.unbind('<Alt-f>')
        self.root.unbind('<Alt-v>')
        self.root.unbind('<Return>')
        self.root.unbind('<Alt-e>')
        self.root.unbind('<Escape>')
        self.root.unbind('<Alt-q>')
    #
        
    def imprimerSater(self):
        return
    #
    
    # Remise à zéro de la saisie utilisateur
    def razSaisie(self):
        self.efGdh.setvalue("")
        self.cbEmetteur.setentry("")
        self.cbDestinataire.setentry("")
        self.cbSysteme.selectitem(0)
        self.cbDatum.selectitem(0)
        self.efCoordX.setvalue("")
        self.efCoordY.setvalue("")
        self.efDir.setvalue("")
        self.efForce.setvalue("")
        self.efComment.setvalue("")


    # Validation de la saisie utilisateur
    def controleSaisie(self):
        #Contrôle de saisie
        if self.efGdh.valid() == False or \
           self.cbEmetteur.valid() == False or \
           self.cbDestinataire.valid() == False or \
           self.efCoordX.valid() == False or \
           self.efCoordY.valid() == False or \
           self.efDir.valid() == False or \
           self.efForce.valid() == False:
            tkMessageBox.showwarning('Contrôle', 'Les champs en rouge sont absents ou incorrects')
            self.fenetre.focus_set()
            return False

        return True
    

    # Affichage de la ligne dans la list-box
    def afficherListe(self, infosSATER):

        vLigne = infosSATER.getLigne(self.root)
        self.lbListe.insert('0', vLigne)
        self.lbListe.see('0')


    # Alimentation de la liste depuis le fichier de log
    def alimListe (self):

        try:
            fic = open (Commun.getFullPath(self.root, Commun.getFicGSat(self.root)),'r')
        except IOError:
            return

        entete = fic.readline() # on n'en fait rien
        
        for line in fic.readlines():
            vData = line.split(';')
            vHeure = vData[0].split (" ")
            vLigne = " " + vHeure[1].ljust(5)+" | " + \
                     vData[1].ljust(10)+" | " + \
                     vData[5].ljust(14)+" | " + \
                     vData[6].ljust(14)+" | "  + \
                     vData[7].ljust(5) +" | " + \
                     vData[8].ljust(5) +" | " + \
                     vData[9].rstrip("\n")
            self.lbListe.insert('0', vLigne)

        self.lbListe.see('0')

        fic.close()

