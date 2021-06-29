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

###################### Creation d'un message Bilan Ambiance.
class FormBilAmb:
    "Classe définissant le formulaire Bilan Ambiance"
    
    def __init__(self, appli):
        "Constructeur de la fenêtre BilAmb"

        self.root = appli # Référence à l'application racine

        # Création de la nouvelle fenêtre
        self.fenetre = Commun.nouvelleFenetre(self.root, "Bilan d'Ambiance SDIS")
        # Fermeture par la case système
        self.fenetre.protocol("WM_DELETE_WINDOW", self.quitterBilAmb)

        # Composants de la fenêtre
        self.dessineBilAmb()
        self.bulleAide()
        
        # Initialisations
        self.razSaisie()

        # Gestion des raccourcis clavier
        self.fenetre.bind('<Alt-v>', self.validerBilAmb)
        self.fenetre.bind('<Return>', self.validerBilAmb)
        self.fenetre.bind('<Alt-n>', self.annulerBilAmb)
        self.fenetre.bind('<Escape>', self.annulerBilAmb)
        self.fenetre.bind('<Alt-q>', self.quitterBilAmb)
        self.stBilan.bind('<Return>', self.notReturn) # On ne valide pas par <Entrée> sur la zone stBilan

        
    def dessineBilAmb(self):

        # variables locales
        vLigne = 1 # N° de ligne pour le positionnement des composants
        vNomBouton = ""
        vIndice = 0
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
        self.ckGdh.select()
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

        Label (vFen,text = "Bilan d'Ambiance", fg = "blue",bg = "orange").grid(row = vLigne, column = 0, columnspan = 9, sticky = E+W)
        vLigne += 1

        Label (vFen,text = "Entête du Message ", fg = "blue",bg = "cyan").grid(row = vLigne, column = 0, columnspan = 9, sticky = E+W)
        vLigne += 1

        Label (vFen, text = "Origine : ").grid(row = vLigne, column = 0, sticky = W )
        self.efOrigine = Pmw.EntryField (vFen, validate = Commun.nonVideValidator)
        self.efOrigine.grid (row = vLigne, column = 1, columnspan = 2, sticky = W)
        vLigne += 1
        Label (vFen, text = "Destinataires Action: ").grid(row = vLigne, column = 0, sticky = W)
        self.efDestAction = Pmw.EntryField (vFen, validate = Commun.nonVideValidator)
        self.efDestAction.grid (row = vLigne, column = 1, columnspan = 3, sticky = E+W)
        Label (vFen, text = "(utilisez le / comme séparateur)").grid(row = vLigne, rowspan = 2, column = 4, columnspan = 8, sticky = W)
        vLigne += 1
        Label (vFen, text = "Destinataires Info: ").grid(row = vLigne, column = 0, sticky = W)
        self.eDestInfo = Entry(vFen)
        self.eDestInfo.grid (row = vLigne, column = 1, columnspan = 3, sticky = E+W)
        vLigne += 1
        Label (vFen, text = "Degré d'Urgence : ").grid(row = vLigne, column = 0, sticky = W )
        self.cbDegUrg = Commun.comboWidget (self.root, vFen, self.root.cfgListe['DegUrgOBNT'])
        self.cbDegUrg.grid (row = vLigne, column = 1, columnspan = 2, sticky = W)
        vLigne += 1

        Label (vFen, text = "Corps du message ", fg = "blue",bg = "cyan" ).grid(row = vLigne, column = 0,columnspan = 8, sticky = E+W)
        vLigne += 1
        Label (vFen, text = "Objet : ").grid(row = vLigne, column = 0, sticky = W)
        self.efObjet = Pmw.EntryField (vFen, validate = Commun.nonVideValidator)
        self.efObjet.grid (row = vLigne, column = 1, columnspan = 6, sticky = W+E)
        vLigne += 1
        
        Label ( vFen, text = "Localisation précise : ").grid(row = vLigne, column = 0, sticky = W)
        self.eLoc = Entry (vFen)
        self.eLoc.grid (row = vLigne, column = 1, columnspan = 6, sticky = E+W)
        vLigne += 1

        Label ( vFen, text = "Bilan circonstancié : " ).grid(row = vLigne, column = 0, sticky = W)
        self.stBilan = ScrolledText (vFen, wrap = "word", height = 5, width = 80)
        self.stBilan.grid (row = vLigne, column = 1, columnspan = 7, sticky = W)
        vLigne += 5

        Label (vFen,text = "Final du message ", fg = "blue",bg = "cyan").grid(row = vLigne, column = 0, columnspan = 8, sticky = E+W)
        vLigne += 1
        Label (vFen, text = "GDH Dépôt/Rédaction : ").grid(row = vLigne, column = 0, sticky = W )
        self.efGdhDep = Commun.gdhWidget(vFen, vFen)
        self.efGdhDep.grid (row = vLigne, column = 1, sticky = W)
        self.rbACK = Pmw.RadioSelect(vFen, buttontype = "radiobutton",labelpos = W,label_text = "Demande Accusé de Réception : ")
        self.rbACK.grid(row = vLigne, column = 3, columnspan = 4, sticky = W)
        self.rbACK.add("Oui")
        self.rbACK.add("Non")
        vLigne += 1
      
        Label (vFen,text = "Fin de Message", fg = "blue",bg = "orange").grid(row = vLigne, column = 0, columnspan = 8, sticky = E+W)
        vLigne += 1

        Button (vFen, text = "Valider", command = self.validerBilAmb, fg = "red", underline = 0).grid(row = vLigne, column = 1, padx = 5,pady = 5, sticky = E+W)
        Button (vFen, text = "Annuler", command = self.annulerBilAmb, fg = "red", underline = 1).grid(row = vLigne, column = 3, padx = 5,pady = 5, sticky = E+W)
        Button (vFen, text = "Quitter", command = self.quitterBilAmb, fg = "red", underline = 0).grid(row = vLigne, column = 5, padx = 5,pady = 5, sticky = E+W)
        

    # Définition des bulles d'aide sur la fenêtre
    def bulleAide(self):
        # ATTENTION, les message d'aide des Widgets GesADRA sont déjà gérés
        self.fenetre.bulle.bind(self.stBilan, "Texte du message, sur plusieurs lignes si besoin")
        

    # Action sur un bouton "Valider"
    def validerBilAmb(self, evt = None):
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
        self.redigerBilAmb()

        # Impression
        if self.root.userData['IMPR_MSG'] == "OUI" :
            os.startfile(Commun.getFullPath(self.root, self.vFicBilAmb+".TXT"), "print")
        else :
            tkMessageBox.showinfo('Bilan Ambiance', 'Message créé : ' + self.vFicBilAmb)

        self.fenetre.destroy()

        
    # Action sur le bouton "Annuler"
    def annulerBilAmb(self, evt = None):
        "Traitement du bouton 'Annuler'"
        # Remise à Zéro de la saisie
        self.razSaisie()


    # Action sur le bouton "Quitter"
    def quitterBilAmb(self, evt = None):
        "Traitement du bouton 'Quitter'"
        etesVousSur = tkMessageBox.askquestion("Fermeture du Formulaire", \
                                               "Confirmez-vous la fermeture du Bilan Ambiance ?")
        if etesVousSur == "yes" :
            self.fenetre.destroy()
        else:
            self.fenetre.focus_set()
            

    # Traitement du bind <Return> spécifique
    def notReturn (self, evt = None):
        """Reproduire le comportement normal de la touche <Entrée> pour un ScrolledText"""
        self.stBilan.insert(self.stBilan.index(INSERT), "\n")
        return "break"
        

    # Remise à zéro de la saisie utilisateur
    def razSaisie(self):
        vGdh = datetime.datetime.now().strftime("%d/%m/%y %H:%M")
        self.efGdh.setvalue(vGdh)
        self.ckGdh.select() 
        self.cbEmetteur.setentry("")
        self.cbDestinataire.setentry("")
        self.eInstruc.delete(0,END)
        self.efOrigine.setvalue("")
        self.efDestAction.setvalue("")
        self.eDestInfo.delete(0,END)
        self.cbDegUrg.selectitem(self.root.userData['URG_BILAMB'])
        vTime = datetime.datetime.now().strftime("%H:%M")
        self.efObjet.setvalue(u"Bilan circonstancié à " + vTime)
        self.eLoc.delete(0, END)
        self.stBilan.delete(1.0,END)
        self.efGdhDep.setvalue(vGdh)
        self.rbACK.invoke("Non")
        

    # Validation de la saisie utilisateur
    def controleSaisie(self):
        #Contrôle de saisie
        if not (self.efGdh.valid() and self.cbEmetteur.valid() and self.cbDestinataire.valid() and \
                self.efOrigine.valid() and self.efDestAction.valid()and self.efObjet.valid()):
            tkMessageBox.showwarning('Contrôle', 'Les champs en rouge sont absents ou incorrects')
            self.fenetre.focus_set()
            return False
       
        if self.stBilan.get(1.0, END).strip() == "":
            tkMessageBox.showwarning('Controle', 'Message vide')
            self.stBilan.focus_set()
            return False

        return True


    def redigerBilAmb(self):

        # Nom du fichier
        self.vFicBilAmb = Commun.getFicBilAmb(self.root)
        # Fichier TXT
        self.txtFileBilAmb()
        # Fichier XML
        self.xmlFileBilAmb()
        
        # Ecriture d'une ligne dans la main courante
        vTexte = "Message " + self.vFicBilAmb + \
		         " de " + self.efOrigine.getvalue() + " vers " +  self.efDestAction.getvalue()
        infosMCI = Commun.InfosMCI(self.efGdh.getvalue(), self.cbEmetteur.get(), self.cbDestinataire.get(), \
                                   self.cbDegUrg.get(), " ", vTexte)
        infosMCI.ecrire(self.root)
        
    
    def txtFileBilAmb(self):
        
        fic = open(Commun.getFullPath(self.root, self.vFicBilAmb)+".TXT",'w')

        fic.write(self.vFicBilAmb+"\n\n")
        fic.write('################################################################################\n')
        fic.write('- ' +(self.root.userData['ACTIVATION'] + ' - ')*3+'\n')
        fic.write('--------------------------------------------------------------------------------\n')

        # Informations transmission
        fic.write("GDH Emission : " + self.efGdh.getvalue()+"\n")
        fic.write("Emis par     : " + self.cbEmetteur.get()+"\n")
        fic.write("Recu par     : " + self.cbDestinataire.get()+"\n")
        fic.write("Instructions : " + self.eInstruc.get()+"\n")
        fic.write('================================================================================\n')

        # Entête du message
        fic.write("BILAN D'AMBIANCE".center(80) + "\n")
        fic.write("Origine      : " + self.efOrigine.getvalue()+"\n")
        fic.write("Dest. Action : " + self.efDestAction.getvalue()+"\n")
        fic.write("Dest. Info   : " + self.eDestInfo.get()+"\n")
        fic.write("Urgence      : " + self.cbDegUrg.get()+"\n")
        fic.write('--------------------------------------------------------------------------------\n')

        # Corps du message
        fic.write("Objet        : " + self.efObjet.getvalue()+"\n")
        fic.write("Localisation : " + self.eLoc.get()+"\n")
        fic.write("Bilan circonstancié : \n\n")
        # découpage des lignes du message
        for ligne in self.stBilan.get(1.0,END).split("\n"):
            if len(ligne) > 79:
                for ligne in textwrap.wrap(ligne,79):
                    fic.write(ligne +"\n")
            else:
               fic.write(ligne + "\n")
        fic.write('--------------------------------------------------------------------------------\n')

        # Final du message
        fic.write("GDH Dépôt    : " + self.efGdhDep.getvalue()+"\n")
        fic.write("Demande A.R. : " + self.rbACK.getvalue()+"\n")
        fic.write("FIN DE MESSAGE".center(80) + "\n")
        fic.write('================================================================================\n')
        fic.write('- ' +(self.root.userData['ACTIVATION'] + ' - ')*3+'\n')
        fic.write('################################################################################\n')

        fic.close()

    #
    def xmlFileBilAmb(self):

        fic = open(Commun.getFullPath(self.root, self.vFicBilAmb+".XML"),'w')
        
        fic.write('<?xml version="1.0" encoding="iso-8859-15"?><?xml-stylesheet type="text/xsl" href="..\msgBilAmb.XSL"?>\n')
        fic.write('<msg>\n')
        fic.write('<form>Message BilAmb</form>\n')
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
        fic.write("<obj>" + self.efObjet.get()+"</obj>\n")
        fic.write("<local>" + self.eLoc.get()+"</local>\n")
        # découpage des lignes du message
        for ligne in self.stBilan.get(1.0,END).split("\n"):
            if len(ligne) > 79:
                for ligne in textwrap.wrap(ligne,79):
                    fic.write("<txt>" + ligne +"</txt>\n")
            else:
               fic.write("<txt>" + ligne + "</txt>\n")
        fic.write('</corps>\n')
        fic.write('<bot>\n')
        fic.write("<gdh>" + self.efGdhDep.getvalue()+"</gdh>\n")
        fic.write("<ack>" + self.rbACK.getvalue()+"</ack>\n")
        fic.write('</bot>\n')
            
        fic.write('</msg>\n')
    
        fic.close()
    #