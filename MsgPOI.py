# -*- coding: iso-8859-15 -*-

from tkinter import *
from tkinter.scrolledtext import ScrolledText
 
import datetime
import time
import os
import tkinter.messagebox as tkMessageBox
import Pmw
import Commun # Module principal des fonctions annexes

###################### Creation nouveau releve carto
class FormPOI:
    "Classe d�finissant le formulaire Point Particulier"
    
    def __init__(self, appli):
        "Constructeur de la fen�tre POI"

        self.root = appli # R�f�rence � l'application racine

        # Cr�ation de la nouvelle fen�tre
        self.fenetre = Commun.nouvelleFenetre(self.root, "Message Point Particulier (POI)")
        # Param�trage sp�cifique de la fen�tre
        self.fenetre.protocol("WM_DELETE_WINDOW", self.quitterPOI)

        # Composants de la fen�tre
        self.dessinePOI()

        # Initialisations
        self.razSaisie()
        
        # Gestion des raccourcis clavier
        self.fenetre.bind('<Alt-v>', self.validerPOI)
        self.fenetre.bind('<Return>', self.validerPOI)
        self.fenetre.bind('<Alt-n>', self.annulerPOI)
        self.fenetre.bind('<Escape>', self.annulerPOI)
        self.fenetre.bind('<Alt-q>', self.quitterPOI)
        
        
    def dessinePOI(self):

        # variables locales
        vLigne = 1 # N� de ligne pour le positionnement des composants
        vFen = self.fenetre

        # Composants de la fen�tre
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
        
        Label (vFen, text = "Degr� d'Urgence : ").grid(row = vLigne, column = 0, sticky = W )
        self.cbDegUrg = Commun.comboWidget (self.root, vFen, self.root.cfgListe['DegUrgOBNT'])
        self.cbDegUrg.grid (row = vLigne, column = 1, columnspan = 2, sticky = W)
        vLigne += 1

        Label (vFen, text = "Instructions particuli�res : ").grid(row = vLigne, column = 0, sticky = W)
        self.eInstruc = Entry (vFen)
        self.eInstruc.grid (row = vLigne, column = 1, columnspan = 4, sticky = W+E)
        vLigne += 1
        
        Label (vFen,text = "Informations Point Particulier", fg = "blue",bg = "orange").grid(row = vLigne, column = 0, columnspan = 8, sticky = W+E)
        vLigne += 1
        
        Label (vFen, text = "Syst�me : ").grid(row = vLigne, column = 0, sticky = W )
        self.cbSysteme = Commun.comboWidget (self.root, vFen, self.root.cfgListe['Systeme'])
        self.cbSysteme.grid (row = vLigne, column = 1, columnspan = 2, sticky = W)
        Label (vFen, text = "Datum : ").grid(row = vLigne, column = 3, sticky = W )
        self.cbDatum = Commun.comboWidget (self.root, vFen, self.root.cfgListe['Datum'])
        self.cbDatum.grid (row = vLigne, column = 4, columnspan = 2, sticky = W)
        vLigne += 1

        Label (vFen, text = "Coordonn�e X :").grid(row = vLigne, column = 0, sticky = W)
        self.efCoordX = Commun.coordWidget(self.root, vFen)
        self.efCoordX.grid (row = vLigne, column = 1, sticky = W)
        Label (vFen, text = "Coordonn�e Y :").grid(row = vLigne, column = 3, sticky = W)
        self.efCoordY = Commun.coordWidget(self.root, vFen)
        self.efCoordY.grid ( row = vLigne, column = 4, sticky = W)
        vLigne += 1

        Label (vFen, text = "Type de point :").grid(row = vLigne, column = 0, sticky = W)
        self.cbTypReleve = Pmw.ComboBox (vFen, scrolledlist_items = self.root.cfgListe['TypReleve'], listheight = 100)
        self.cbTypReleve.grid ( row = vLigne, column = 1, sticky = W+E)
        vLigne += 1

        Label (vFen, text = "Caract�ristiques : " ).grid( row = vLigne, column = 0, sticky = W )
        self.efDetail = Pmw.EntryField(vFen)
        self.efDetail.grid ( row = vLigne, column = 1, columnspan = 4, sticky = W+E)
        vLigne += 1
    
        Label (vFen,text = "Commentaire : ").grid(row = vLigne, column = 0, sticky = W)
        self.eTexte = Entry (vFen)
        self.eTexte.grid (row = vLigne, column = 1, columnspan = 4, sticky = E+W)
        vLigne += 3
    
        Label (vFen,text = "Fin de message ", fg = "blue",bg = "orange").grid(row = vLigne, column = 0, columnspan = 12, sticky = E+W)
        vLigne += 1

        Button (vFen, text="Valider", command = self.validerPOI, fg="red", underline = 0).grid(row=vLigne, column=0, padx=5, pady=5)
        Button (vFen, text="Annuler", command = self.annulerPOI, fg="red", underline = 1).grid(row=vLigne, column=2, padx=5, pady=5)
        Button (vFen, text="Quitter", command = self.quitterPOI, fg="red", underline = 0).grid(row=vLigne, column=4, padx=5, pady=5)


    # D�finition des bulles d'aide sur la fen�tre
    def bulleAide(self):
        # ATTENTION, les message d'aide des Widgets GesADRA sont d�j� g�r�s
        return
    

    # Action sur un bouton "Valider"
    def validerPOI(self, evt = None):
        "Traitement du bouton 'Valider'"

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
        self.redigerPOI()

        # Impression
        if self.root.userData['IMPR_MSG'] == "OUI" :
            os.startfile(Commun.getFullPath(self.root, self.vFicPOI+".TXT"), "print")
        else :
            tkMessageBox.showinfo('Message Point Particulier', 'Message cr�� : ' + self.vFicPOI)

        self.fenetre.destroy()

        
    # Action sur le bouton "Annuler"
    def annulerPOI(self, evt = None):
        "Traitement du bouton 'Annuler'"
        # Remise � Z�ro de la saisie
        self.razSaisie()


    # Action sur le bouton "Quitter"
    def quitterPOI(self, evt = None):
        "Traitement du bouton 'Quitter'"
        etesVousSur = tkMessageBox.askquestion("Fermeture du Formulaire", \
                                               "Confirmez-vous la fermeture du Message POI ?")
        if etesVousSur == "yes" :
            self.fenetre.destroy()
        else:
            self.fenetre.focus_set()


    # Remise � z�ro de la saisie utilisateur
    def razSaisie(self):
        vGdh = datetime.datetime.now().strftime("%d/%m/%y %H:%M")
        self.efGdh.setvalue(vGdh) 
        self.ckGdh.select()
        self.cbDegUrg.selectitem(self.root.userData['URG_POI'])
        self.eInstruc.delete(0,END)
        self.cbEmetteur.setentry("")
        self.cbDestinataire.setentry("")
        self.cbSysteme.selectitem(0)
        self.cbDatum.selectitem(0)
        self.efCoordX.setvalue("")
        self.efCoordY.setvalue("")
        self.cbTypReleve.selectitem(0)
        self.efDetail.setentry("")
        self.eTexte.delete(0, END)


    # Validation de la saisie utilisateur
    def controleSaisie(self):
        if self.efGdh.valid() == False or \
           self.cbEmetteur.valid() == False or \
           self.cbDestinataire.valid() == False or \
           self.efCoordX.valid() == False or \
           self.efCoordY.valid() == False or \
           self.efDetail.valid() == False :
            tkMessageBox.showwarning('Contr�le', 'Les champs en rouge sont absents ou incorrects')
            self.fenetre.focus_set()
            return False

        return True
    
        
    ##Creation nouveau MSG POI ###################################################
    def redigerPOI(self):

        # Nom du fichier
        self.vFicPOI = Commun.getFicPOI(self.root)
        # Fichier TXT
        self.txtFilePOI()
        # Fichier XML
        self.xmlFilePOI()
        
        # Ecriture d'une ligne dans la main courante
        vTexte = "Message " + self.vFicPOI
        infosMCI = Commun.InfosMCI(self.efGdh.getvalue(), self.cbEmetteur.get(), self.cbDestinataire.get(), \
                                   self.cbDegUrg.get(), " ", vTexte)
        infosMCI.ecrire(self.root)
        
    
    def txtFilePOI(self):
        
        fic = open(Commun.getFullPath(self.root, self.vFicPOI+".TXT"),'w')
        
        fic.write(self.vFicPOI+"\n\n")
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
        fic.write("MESSAGE POINT PARTICULIER".center(80) + "\n")

        fic.write("Syst�me      : " + self.cbSysteme.get()+"\n")
        fic.write("Datum        : " + self.cbDatum.get()+"\n")
        fic.write("Coordonn�e X : " + self.efCoordX.getvalue()+"\n")
        fic.write("Coordonn�e Y : " + self.efCoordY.getvalue()+"\n")
        fic.write("Type relev�  : " + self.cbTypReleve.get()+"\n")
        fic.write("Caract�rist. : " + self.efDetail.getvalue()+"\n")
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
    def xmlFilePOI(self):

        fic = open(Commun.getFullPath(self.root, self.vFicPOI+".XML"),'w')
        
        fic.write('<?xml version="1.0" encoding="iso-8859-15"?><?xml-stylesheet type="text/xsl" href="..\msgPOI.XSL"?>\n')
        fic.write('<msg>\n')
        fic.write('<form>Message POI</form>\n')
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
        fic.write("<typrel>" + self.cbTypReleve.get()+"</typrel>\n")
        fic.write("<detail>" + self.efDetail.getvalue()+"</detail>\n")
        fic.write("<txt>" + self.eTexte.get()+"</txt>\n")
        fic.write('</corps>\n')
            
        fic.write('</msg>\n')
    
        fic.close()
    #
