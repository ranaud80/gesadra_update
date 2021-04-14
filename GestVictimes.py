# -*- coding: iso-8859-15 -*-

from Tkinter import *
from ScrolledText import ScrolledText

import datetime
import time
import os
import tkMessageBox
import tkSimpleDialog
import tkFont 
import Pmw
import Commun # Module principal des fonctions annexes

###################### Creation nouveau releve carto
class FormGVict:
    "Classe définissant le formulaire Victimes"
    
    def __init__(self, appli):
        """Constructeur de la fenêtre Vict"""

        self.root = appli # Référence à l'application racine
        self.fenetre = self.root.notebook.add('Liste des Victimes')
        self.boutonE = [] # liste des boutons EMETTEUR

        # Composants de la fenêtre
        self.drawGVict()
        self.bulleAide()
        
        # Initialisations
        self.razSaisie()
        
        # Alimentation de la liste
        self.alimListe()     
        
        # Gestion des raccourcis clavier
        self.selectTab()
        
    def drawGVict(self):

        # variables locales
        vLigne = 1 # N° de ligne pour le positionnement des composants
        vFen = self.fenetre

        # Le label zone cachée "réserve" la place du bouton[0] dans le gridder
        Label (vFen,text = "zone cachée", bg = "orange",width=9).grid(row = vLigne, column = 1, sticky = E+W)
        Label (vFen,text = "Stations présentes sur le réseau", fg = "blue",bg = "orange").grid(row = vLigne, column = 0,columnspan = 16, sticky = E+W)
        vLigne += 1
        # 14 boutons "Emetteur"
        Label (vFen, text = "Reçu de :").grid(row = vLigne, column = 0)
        for indice in range(0, 15):
            bouton = Button(vFen, width = 8, foreground = "red", takefocus = 1)
            bouton.grid(column = indice+1, row = vLigne, sticky = E+W)
            bouton.configure(command = lambda x = indice : self.cliquerRecuDe(x))
            if indice == 0: bouton.grid_remove() # Suppression du bouton 0 "Tous"
            self.boutonE.append(bouton)
        vLigne += 1

        # Données des victimes
        Label (vFen,text = "Informations Victime ", fg = "blue",bg = "orange").grid(row = vLigne, column = 0, columnspan = 16, sticky = E+W)
        vLigne += 1
        Label (vFen, text = "Groupe Date/Heure : ").grid(row = vLigne, column = 0, sticky = W)
        self.efGdh = Commun.gdhWidget(self.root, vFen)
        self.efGdh.grid(row = vLigne, column = 1, columnspan = 2, sticky = W)
        self.bGdh = Button(vFen, width = 8, bd = 1, fg = "blue", text = "Forcer", command = self.forcerGDH, underline = 0)
        self.bGdh.grid(row = vLigne, column = 3)
        vLigne += 1

        Label (vFen, text = "Emis par : ").grid(row = vLigne, column = 0, sticky = W)
        self.cbEmetteur = Commun.indicatifWidget(self.root, vFen, self.root)
        self.cbEmetteur.grid (row = vLigne, column = 1, columnspan = 3, sticky = W)
        Label (vFen, text = "Reçu par : ").grid(row = vLigne, column = 4, columnspan = 2, sticky = W)
        self.cbDestinataire = Commun.indicatifWidget(self.root, vFen, self.root)
        self.cbDestinataire.grid (row = vLigne, column = 6, columnspan = 3, sticky = W)
        vLigne += 2
         
        # Victime
        Label (vFen, text = "Num Victime : ").grid(row = vLigne, column = 0,sticky = W) 
        self.efNum = Pmw.EntryField (vFen, validate = {"validator" : Commun.numValidator, "min" : 1, "max" : 99999, "minstrict" : False, "maxstrict" : False})
        self.efNum.component('entry').config(width = 8) 
        self.efNum.grid(row = vLigne, column = 1, sticky = W) 
        self.bNum = Button(vFen, width = 8, bd = 1, fg = "blue", text = "Num. Auto", command = self.numAuto, underline = 0)
        self.bNum.grid(row = vLigne, column = 2)
        Label (vFen, text = "Age / Date naissance :").grid(row = vLigne, column = 4, columnspan = 2, sticky = W )
        self.eAge = Entry(vFen)
        self.eAge.grid (row = vLigne, column = 6, columnspan = 2, sticky = W)
        self.rbSexe = Pmw.RadioSelect(vFen, buttontype = "radiobutton", labelpos = W, label_text = "Sexe :", pady = 0)
        self.rbSexe.grid(row = vLigne, column = 9, columnspan = 3, rowspan = 2, sticky = N+W)
        self.rbSexe.add("H")
        self.rbSexe.add("F")
        vLigne += 1
        Label (vFen, text = "Nom - Prénom : ").grid(row = vLigne, column = 0, sticky = W)
        self.eNom = Entry(vFen)
        self.eNom.grid(row = vLigne, column = 1, columnspan = 7, sticky = W+E)
        vLigne += 1

        # Détresse
        Label (vFen, text = "Nature : ").grid(row = vLigne, column = 0, sticky = W)
        self.cbNature = Pmw.ComboBox (vFen, scrolledlist_items = self.root.cfgListe['Nature'], listheight = 80 )
        self.cbNature.grid(row = vLigne, column = 1, columnspan = 3, sticky = W)
        Label (vFen, text = "Détresse Vitale : ").grid(row = vLigne, column = 4, columnspan = 2, sticky = W)
        self.cbVitale = Pmw.ComboBox (vFen, scrolledlist_items = self.root.cfgListe['Detresse'], listheight = 100 )
        self.cbVitale.grid(row = vLigne, column = 6, columnspan = 3, sticky = W)
        Label (vFen, text = "Tri PMA : ").grid(row = vLigne, column = 9, sticky = W)
        self.cbUrgence = Pmw.ComboBox (vFen, scrolledlist_items = self.root.cfgListe['Urgence'], listheight = 100 )
        self.cbUrgence.grid(row = vLigne, column = 10, columnspan = 3, sticky = W)
        vLigne += 1

        Label (vFen, text = "Autre :" ).grid( row = vLigne, column = 0, sticky = W)
        self.eAutre = Entry(vFen )
        self.eAutre.grid(row = vLigne, column = 1, columnspan = 7, sticky = W+E)
        vLigne += 1
    
        self.bValider = Button (vFen, text = "Valider", command = self.validerGVict, fg = "red", underline = 0)
        self.bValider.grid (row = vLigne, column = 1, columnspan = 2, sticky = E+W, padx = 5,pady = 5 )
        self.bEffacer = Button (vFen, text = "Effacer", command = self.effacerGVict, fg = "red", underline = 0)
        self.bEffacer.grid (row = vLigne, column = 4, columnspan = 2, sticky = E+W, padx = 5,pady = 5)
        self.bQuitter = Button (vFen, text = "Quitter", command = self.quitterGVict, fg = "red", underline = 0)
        self.bQuitter.grid (row = vLigne, column = 7, columnspan = 2, sticky = E+W, padx = 5,pady = 5)
        vLigne += 1

        # Dernières Vicitmes
        Label (vFen,text = "Liste des Victimes", fg = "blue",bg = "orange").grid( row = vLigne, column = 0, columnspan = 16, sticky = E+W)
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
            
    # Définition des bulles d'aide sur la fenêtre
    def bulleAide(self):
        # ATTENTION, les message d'aide des Widgets GesADRA sont déjà gérés
        self.root.bulle.bind(self.efNum, "Nombre de 1 à 5 chiffres ou 'Auto'")


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
            self.efNum.component('entry').focus_set()
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

    # Action sur un bouton "Auto"
    def numAuto(self, evt = None):
        self.efNum.setvalue('Auto')
        
    # Action sur un bouton "Valider"
    def validerGVict(self, evt = None):
        "Traitement du bouton 'Valider'"

        # Contrôle de la validité des données
        if self.controleSaisie() == False: 
            # Si erreur, on stoppe le traitement
            return False

        # Ligne Victime
        infosVict = Commun.InfosVict(self.efGdh.getvalue(), self.efNum.getvalue(), self.eAge.get(), self.rbSexe.getvalue(), \
                                       self.eNom.get(), self.cbNature.get(), self.cbVitale.get(), \
                                       self.cbUrgence.get(), self.eAutre.get())
        infosVict.ecrire(self.root)

        self.afficherListe(infosVict)

        # Ligne de MCI
        vTexte = "Victime :  Num = " + self.efNum.getvalue() + \
                 ", Nature = " + self.cbNature.get() +", Urgence = " + self.cbUrgence.get()
        infosMCI = Commun.InfosMCI(self.efGdh.getvalue(), self.cbEmetteur.get(), self.cbDestinataire.get(),\
                                   self.root.userData['URG_BILSEC'], " ", vTexte)
        infosMCI.ecrire(self.root)
 
        # Remise à Zéro du formulaire
        self.razSaisie()

        
    # Action sur le bouton "Effacer"
    def effacerGVict(self, evt = None):
        """Traitement du bouton 'Effacer'"""
        # Remise à Zéro de la saisie
        self.razSaisie()


    # Action sur le bouton "Effacer"
    def quitterGVict(self, evt=None):
        """Traitement du bouton 'Quitter'"""
        if self.efGdh.getvalue().strip() != "":
            etesVousSur = tkMessageBox.askquestion("Gestion des Victimes", \
                                                   "Saisie en cours.\nConfirmez-vous la fermeture de cet onglet ?")
        else:
            etesVousSur = "yes"
            
        if etesVousSur == "yes" :
            self.root.printMenu.delete(self.root.printMenu.index("Liste Victimes"))
            self.unSelectTab()
            self.root.notebook.delete('Liste des Victimes')
            self.root.fenGVict = None 
            self.fenetre.destroy()
        else:
            self.fenetre.focus_set()

    def createTab(self):
        self.root.printMenu.add_command(label="Liste Victimes", command=self.imprimerVict)
    #
    
    def selectTab(self):
        self.initBoutons()
        
        self.root.bind('<Alt-f>', self.forcerGDH)
        self.root.bind('<Alt-v>', self.validerGVict)
        self.root.bind('<Return>', self.validerGVict)
        self.root.bind('<Alt-e>', self.effacerGVict)
        self.root.bind('<Escape>', self.effacerGVict)
        self.root.bind('<Alt-q>', self.quitterGVict)
        
    #
        
    def unSelectTab(self):
        
        self.root.unbind('<Alt-f>')
        self.root.unbind('<Alt-v>')
        self.root.unbind('<Return>')
        self.root.unbind('<Alt-e>')
        self.root.unbind('<Escape>')
        self.root.unbind('<Alt-q>')
    #
        
    def imprimerVict(self):
        return
    #
    
    # Remise à zéro de la saisie utilisateur
    def razSaisie(self):
        self.efGdh.setvalue("")
        self.cbEmetteur.setentry("")
        self.cbDestinataire.setentry("")
        self.efNum.setvalue("")
        self.eAge.delete(0,END)
        self.rbSexe.selection = None
        self.eNom.delete(0,END)
        self.cbNature.setentry("")
        self.cbVitale.setentry("")
        self.cbUrgence.setentry("")
        self.eAutre.delete(0,END)
 

    # Validation de la saisie utilisateur
    def controleSaisie(self):
        #Contrôle de saisie
        if not (self.efGdh.valid() and self.efNum.valid()):
            tkMessageBox.showwarning('Contrôle', 'Les champs en rouge sont absents ou incorrects')
            self.fenetre.focus_set()
            return False
        if not self.efNum.valid():
            tkMessageBox.showwarning('Contrôle', 'Numéro de victime incorrect')
            self.efNum.focus_set()
            return False
        else:
            if self.efNum.getvalue() == 'Auto':
                self.efNum.setvalue(Commun.getNumVict(self.root))
            else:   
                self.efNum.setvalue(self.efNum.getvalue().zfill(5))
        if self.rbSexe.getvalue() == None:
            tkMessageBox.showwarning('Contrôle', 'Indiquez le sexe de la victime')
            self.rbSexe.focus_set()
            return False
        
        return True 

        
    # Affichage de la ligne dans la list-box
    def afficherListe(self, infosVict):

        vLigne = infosVict.getLigne(self.root)
        self.lbListe.insert('0', vLigne)
        self.lbListe.see('0')


    # Alimentation de la liste depuis le fichier de log
    def alimListe (self):

        try:
            fic = open (Commun.getFullPath(self.root, Commun.getFicGVict(self.root)),'r')
        except IOError:
            return

        entete = fic.readline() # on n'en fait rien
        
        for line in fic.readlines():
            vData = line.split(';')
            vHeure = vData[0].split (" ")
            
            vLigne = " " + vHeure[1].ljust(5)+" | " + \
                     vData[1].ljust(6)+" | " + \
                     vData[2].ljust(10)+" | " + \
                     vData[3].ljust(3)+" | "  + \
                     vData[4].ljust(16) +" | " + \
                     vData[5].ljust(12) +" | " + \
                     vData[6].ljust(12) +" | " + \
                     vData[7].ljust(12) +" | " + \
                     vData[8].rstrip("\n")
            self.lbListe.insert('0', vLigne)

        self.lbListe.see('0')

        fic.close()


