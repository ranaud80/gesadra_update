# -*- coding: iso-8859-15 -*-

from tkinter import *
from tkinter.scrolledtext import ScrolledText

import datetime
import time
import os
import tkinter.messagebox as tkMessageBox
import Pmw
import Commun # Module principal des fonctions annexes

###################### Creation d'un Relev� Sater.
class FormSATER:
    "Classe d�finissant le formulaire Relev� Sater"
    
    def __init__(self, appli):
        "Constructeur de la fen�tre Sater"

        self.root = appli # R�f�rence � l'application racine

        # Cr�ation de la nouvelle fen�tre
        self.fenetre = Commun.nouvelleFenetre(self.root, "Message de Relev� SATER")
        # Param�trage sp�cifique de la fen�tre
        self.fenetre.protocol("WM_DELETE_WINDOW", self.quitterSATER)

        # Composants de la fen�tre
        self.dessineSATER()

        # Initialisations
        self.razSaisie()
        
        # Gestion des raccourcis clavier
        self.fenetre.bind('<Alt-v>', self.validerSATER)
        self.fenetre.bind('<Return>', self.validerSATER)
        self.fenetre.bind('<Alt-n>', self.annulerSATER)
        self.fenetre.bind('<Escape>', self.annulerSATER)
        self.fenetre.bind('<Alt-q>', self.quitterSATER)
        

    def dessineSATER(self):

        # variables locales
        vLigne = 1 
        vFen = self.fenetre

        # Composants de la fenetre
        Label (vFen,text = "Informations Transmission ", fg = "blue",bg = "orange").grid(row = vLigne, column = 0, columnspan = 12, sticky = E+W)
        vLigne += 1
        Label (vFen, text = "Groupe Date/Heure : ").grid(row = vLigne, column = 0, sticky = W)
        self.efGdh = Commun.gdhWidget(vFen, vFen)
        self.efGdh.grid(row = vLigne, column = 1, sticky = W)
        self.iGdh = IntVar()
        self.ckGdh = Checkbutton (vFen, text = "Recalculer le GDH lors de la validation", variable = self.iGdh)
        self.ckGdh.grid(row = vLigne, column = 3, columnspan = 3, sticky = W)
        vLigne += 1
        
        Label (vFen, text = "Emis par : ").grid(row = vLigne, column = 0, sticky = W)
        self.cbEmetteur = Commun.indicatifWidget(vFen, vFen, self.root)
        self.cbEmetteur.grid (row = vLigne, column = 1, sticky = W)
        Label (vFen, text = "Re�u par : ").grid(row = vLigne, column = 3, sticky = W)
        self.cbDestinataire = Commun.indicatifWidget(vFen, vFen, self.root)
        self.cbDestinataire.grid (row = vLigne, column = 4, sticky = W)
        vLigne += 1
        
        Label (vFen, text = "Degr� d'Urgence : ").grid(row = vLigne, column = 0, sticky = W)
        self.cbDegUrg = Commun.comboWidget (self.root, vFen, self.root.cfgListe['DegUrgOBNT'])
        self.cbDegUrg.grid (row = vLigne, column = 1, columnspan = 2, sticky = W)
        vLigne += 1

        Label (vFen, text = "Instructions particuli�res : ").grid(row = vLigne, column = 0, sticky = W)
        self.eInstruc = Entry (vFen)
        self.eInstruc.grid (row = vLigne, column = 1, columnspan = 4, sticky = W+E)
        vLigne += 1
         
        Label (vFen,text = "Informations Relev� Sater", fg = "blue",bg = "orange").grid(row = vLigne, column = 0, columnspan = 12, sticky = E+W)
        vLigne += 1

        Label (vFen, text = "Syst�me : ").grid(row = vLigne, column = 0, sticky = W)
        self.cbSysteme = Commun.comboWidget (self.root, vFen, self.root.cfgListe['Systeme'])
        self.cbSysteme.grid (row = vLigne, column = 1, columnspan = 2, sticky = W)
        Label (vFen, text = "Datum : ").grid(row = vLigne, column = 3, sticky = W)
        self.cbDatum = Commun.comboWidget (self.root, vFen, self.root.cfgListe['Datum'])
        self.cbDatum.grid (row = vLigne, column = 4, columnspan = 2, sticky = W)
        vLigne += 1

        Label (vFen, text = "Coordonn�e X :").grid(row = vLigne, column = 0, sticky = W)
        self.efCoordX = Commun.coordWidget(self.root, vFen)
        self.efCoordX.grid (row = vLigne, column = 1, sticky = W)
        Label (vFen, text = "Coordonn�e Y :").grid(row = vLigne, column = 3, sticky = W)
        self.efCoordY = Commun.coordWidget(self.root, vFen)
        self.efCoordY.grid (row = vLigne, column = 4, sticky = W)
        vLigne += 1

        Label (vFen, text = "Direction du relev� :").grid(row = vLigne, column = 0, sticky = W)
        self.efDir = Pmw.EntryField (vFen, validate = Commun.nonVideValidator)
        self.efDir.grid(row = vLigne, column = 1, sticky = W)
        Label (vFen, text = "Force du signal :").grid(row = vLigne, column = 3, sticky = W)
        self.eForce = Entry (vFen)
        self.eForce.grid(row = vLigne, column = 4, sticky = W)
        vLigne += 1

        Label (vFen, text = "Commentaire : " ).grid( row = vLigne, column = 0, sticky = W)
        self.eTexte = Entry(vFen)
        self.eTexte.grid ( row = vLigne, column = 1, columnspan = 9, sticky = E+W)
        vLigne += 1


        Label (vFen,text = "Fin de message ", fg = "blue",bg = "orange").grid(row = vLigne, column = 0, columnspan = 12, sticky = E+W)
        vLigne += 1
        
        Button (vFen, text="Valider", command = self.validerSATER, fg="red", underline = 0).grid(row=vLigne, column=0, padx=5, pady=5)
        Button (vFen, text="Annuler", command = self.annulerSATER, fg="red", underline = 1).grid(row=vLigne, column=2, padx=5, pady=5)
        Button (vFen, text="Quitter", command = self.quitterSATER, fg="red", underline = 0).grid(row=vLigne, column=4, padx=5, pady=5)


    # D�finition des bulles d'aide sur la fen�tre
    def bulleAide(self):
        # ATTENTION, les message d'aide des Widgets GesADRA sont d�j� g�r�s
        return
    

    # Action sur un bouton "Valider"
    def validerSATER(self, evt = None):
        """Traitement du bouton 'Valider'"""

        #Contr�le de la validit� des donn�es
        if self.controleSaisie() == False:
            # Si erreur, on stoppe le traitement
            return False

        # Recalcul des donn�es variables (Gdh, N� message, etc...)
        if self.iGdh.get() == True :
            self.efGdh.setvalue("")
            vGdh = datetime.datetime.now().strftime("%d/%m/%y %H:%M")
            self.efGdh.setvalue(vGdh)

        # R�daction du message
        self.redigerSATER()

        # Impression
        if self.root.userData['IMPR_MSG'] == "OUI" :
            os.startfile(Commun.getFullPath(self.root, self.vFicSATER+".TXT"), "print")
        else :
            tkMessageBox.showinfo('Message SATER', 'Message cr�� : ' + self.vFicSATER)

        self.fenetre.destroy()

        
    # Action sur le bouton "Annuler"
    def annulerSATER(self, evt = None):
        """Traitement du bouton 'Annuler'"""
        # Remise � Z�ro de la saisie
        self.razSaisie()


    # Action sur le bouton "Quitter"
    def quitterSATER(self, evt = None):
        """Traitement du bouton 'Quitter'"""
        etesVousSur = tkMessageBox.askquestion("Fermeture du Formulaire", \
                                               "Confirmez-vous la fermeture du Message Sater ?")
        if etesVousSur == "yes" :
            self.fenetre.destroy()
        else:
            self.fenetre.focus_set()


    # Remise � z�ro de la saisie utilisateur
    def razSaisie(self):
        vGdh = datetime.datetime.now().strftime("%d/%m/%y %H:%M")
        self.efGdh.setvalue(vGdh) 
        self.ckGdh.select()
        self.cbDegUrg.selectitem(self.root.userData['URG_SATER'])
        self.eInstruc.delete(0,END)
        self.cbEmetteur.setentry("")
        self.cbDestinataire.setentry("")
        self.cbSysteme.selectitem(0)
        self.cbDatum.selectitem(0)
        self.efCoordX.setvalue("")
        self.efCoordY.setvalue("")
        self.efDir.setvalue("")
        self.eForce.delete(0, END)
        self.eTexte.delete(0, END)


    # Validation de la saisie utilisateur
    def controleSaisie(self):
        #Contr�le de saisie
        if self.efGdh.valid() == False or \
           self.cbEmetteur.valid() == False or \
           self.cbDestinataire.valid() == False or \
           self.efCoordX.valid() == False or \
           self.efCoordY.valid() == False or \
           self.efDir.valid() == False :
            tkMessageBox.showwarning('Contr�le', 'Les champs en rouge sont absents ou incorrects')
            self.fenetre.focus_set()
            return False

        return True
    

    ##Creation nouveau MSG SATER ###################################################
    def redigerSATER(self):

        # Nom du fichier
        self.vFicSATER = Commun.getFicSATER(self.root)
        # Fichier TXT
        self.txtFileSATER()
        # Fichier XML
        self.xmlFileSATER()
        
        # Ecriture d'une ligne dans la main courante
        vTexte = "Message " + self.vFicSATER
        infosMCI = Commun.InfosMCI(self.efGdh.getvalue(), self.cbEmetteur.get(), self.cbDestinataire.get(), \
                                   self.cbDegUrg.get(), " ", vTexte)
        infosMCI.ecrire(self.root)
        
    
    def txtFileSATER(self):
        
        fic = open(Commun.getFullPath(self.root, self.vFicSATER+".TXT"),'w')
        
        fic.write(self.vFicSATER+"\n\n")
        fic.write('################################################################################\n')
        fic.write('- ' +(self.root.userData['ACTIVATION'] + ' - ')*3+'\n')
        fic.write('--------------------------------------------------------------------------------\n')

        # Informations transmission
        fic.write("GDH Emission : " + self.efGdh.getvalue()+"\n")
        fic.write("Emis par     : " + self.cbEmetteur.get()+"\n")
        fic.write("Recu par     : " + self.cbDestinataire.get()+"\n")
        fic.write("Urgence      : " + self.cbDegUrg.get()+"\n")
        fic.write("Instructions : " + self.eInstruc.get()+"\n")
        fic.write('================================================================================\n')

        # Corps du message
        fic.write("MESSAGE RELEVE SATER".center(80) + "\n")
        fic.write("Syst�me      : " + self.cbSysteme.get()+"\n")
        fic.write("Datum        : " + self.cbDatum.get()+"\n")
        fic.write("Coordonn�e X : " + self.efCoordX.getvalue()+"\n")
        fic.write("Coordonn�e Y : " + self.efCoordY.getvalue()+"\n")
        fic.write("Direction    : " + self.efDir.getvalue()+"\n")
        fic.write("Force signal : " + self.eForce.get()+"\n")
        fic.write('--------------------------------------------------------------------------------\n')
        fic.write("Commentaire  : \n")
        fic.write(self.eTexte.get()+"\n")
        fic.write('--------------------------------------------------------------------------------\n')

        # Final du message
        fic.write("FIN DE MESSAGE".center(80) + "\n")
        fic.write('================================================================================\n')
        fic.write('- ' +(self.root.userData['ACTIVATION'] + ' - ')*3+'\n')
        fic.write('################################################################################\n')

        fic.close()

    #
    def xmlFileSATER(self):

        fic = open(Commun.getFullPath(self.root, self.vFicSATER+".XML"),'w')
        
        fic.write('<?xml version="1.0" encoding="iso-8859-15"?><?xml-stylesheet type="text/xsl" href="..\msgSATER.XSL"?>\n')
        fic.write('<msg>\n')
        fic.write('<form>Message SATER</form>\n')
        fic.write('<soft>' + self.root.userData['LOGICIEL'] + '</soft>\n')
        fic.write('<vers>' + self.root.userData['VERSION'] + '</vers>\n')
        fic.write('<mode>' + self.root.userData['ACTIVATION'] + '</mode>\n')
        fic.write('<trans>\n')
        fic.write('<gdh>' + self.efGdh.getvalue()+'</gdh>\n')
        fic.write('<emis>' + self.cbEmetteur.get()+'</emis>\n')
        fic.write('<recu>' + self.cbDestinataire.get()+"</recu>\n")
        fic.write("<instr>" + self.eInstruc.get()+"</instr>\n")
        fic.write('</trans>\n')
        fic.write("<corps>\n")
        fic.write("<sys>" + self.cbSysteme.get()+"</sys>\n")
        fic.write("<datum>" + self.cbDatum.get()+"</datum>\n")
        fic.write("<coordx>" + self.efCoordX.getvalue()+"</coordx>\n")
        fic.write("<coordy>" + self.efCoordY.getvalue()+"</coordy>\n")
        fic.write("<dir>" + self.efDir.getvalue()+"</dir>\n")
        fic.write("<force>" + self.eForce.get()+"</force>\n")
        fic.write("<txt>" + self.eTexte.get()+"</txt>\n")
        fic.write('</corps>\n')
            
        fic.write('</msg>\n')
    
        fic.close()
    #

