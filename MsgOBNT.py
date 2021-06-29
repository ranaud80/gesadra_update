# -*- coding: iso-8859-15 -*-

from tkinter import *
from tkinter.scrolledtext import ScrolledText
import textwrap
 
import datetime
import time
import os
import tkinter.messagebox as tkMessageBox
import tkinter.font as tkFont
import Pmw
import Commun # Module principal des fonctions annexes


###################### Creation d'un message OBNT.
class FormOBNT:
    "Classe d�finissant le formulaire OBNT"
    
    def __init__(self, appli):
        "Constructeur de la fen�tre OBNT"

        self.root = appli # R�f�rence � l'application racine

        # Cr�ation de la nouvelle fen�tre
        self.fenetre = Commun.nouvelleFenetre(self.root, "Message standard OBNT")
        # Fermeture par la case syst�me
        self.fenetre.protocol("WM_DELETE_WINDOW", self.quitterOBNT)

        # Composants de la fen�tre
        self.dessineOBNT()
        self.bulleAide()

        # Initialisations
        self.razSaisie()
        
        # Gestion des raccourcis clavier
        self.fenetre.bind('<Alt-v>', self.validerOBNT)
        self.fenetre.bind('<Return>', self.validerOBNT)
        self.fenetre.bind('<Alt-n>', self.annulerOBNT)
        self.fenetre.bind('<Escape>', self.annulerOBNT)
        self.fenetre.bind('<Alt-q>', self.quitterOBNT)
        self.stMessage.bind('<Return>', self.notReturn) # On ne valide pas par <Entr�e> sur la zone stMessage


    def dessineOBNT(self):

        # variables locales
        vLigne = 1 # N� de ligne pour le positionnement des composants
        vNomBouton = ""
        vIndice = 0
        vFen = self.fenetre

        # Composants de la fen�tre
        Label (vFen,text="Informations transmission", fg="blue",bg="orange").grid(row=vLigne, column=0, columnspan=8, sticky=E+W)
        vLigne += 1

        Label (vFen, text="Groupe Date/Heure : ").grid(row=vLigne, column=0, sticky=W)
        self.efGdh = Commun.gdhWidget(vFen, vFen)
        self.efGdh.grid(row=vLigne, column=1, sticky=W)
        self.iGdh = IntVar()
        self.ckGdh = Checkbutton (vFen, text="Recalculer le GDH lors de la validation", variable=self.iGdh)
        self.ckGdh.grid(row=vLigne, column=2, columnspan=2, sticky=W)
        vLigne += 1
        Label (vFen, text="Emis par : ").grid(row=vLigne, column=0, sticky=W)
        self.cbEmetteur = Commun.indicatifWidget(vFen, vFen, self.root)
        self.cbEmetteur.grid (row=vLigne, column=1, sticky=W)
        Label (vFen, text="Re�u par : ").grid(row=vLigne, column=2, sticky=W)
        self.cbDestinataire = Commun.indicatifWidget(vFen, vFen, self.root)
        self.cbDestinataire.grid (row=vLigne, column=3, sticky=W)
        vLigne += 1
        Label (vFen, text="Instructions particuli�res : ").grid(row=vLigne, column=0, sticky=W)
        self.eInstruc = Entry (vFen)
        self.eInstruc.grid (row=vLigne, column=1, columnspan=3, sticky=W+E)
        vLigne += 1

        Label (vFen, text="Message OBNT", fg="blue",bg="orange").grid(row=vLigne, column=0, columnspan=8, sticky=E+W)
        vLigne += 1

        Label (vFen, text="Ent�te du message", fg="blue",bg="cyan").grid(row=vLigne, column=0, columnspan=6, sticky=E+W)
        vLigne += 1
        Label (vFen, text="Origine : ").grid(row=vLigne, column=0, sticky=W)
        self.efOrigine = Pmw.EntryField (vFen, validate=Commun.nonVideValidator)
        self.efOrigine.grid (row= vLigne, column=1 ,sticky=W)
        vLigne += 1
        Label (vFen, text="Destinataires Action : ").grid(row=vLigne, column=0, sticky=W)
        self.efDestAction = Pmw.EntryField (vFen, validate=Commun.nonVideValidator)
        self.efDestAction.grid (row=vLigne, column=1, columnspan=2, sticky=E+W)
        Label (vFen, text="(utilisez le / comme s�parateur)").grid(row=vLigne, rowspan=2, column=3, columnspan=2, sticky=W)
        vLigne += 1
        Label (vFen, text="Destinataires Info : ").grid(row=vLigne, column=0, sticky=W)
        self.eDestInfo = Entry (vFen)
        self.eDestInfo.grid (row=vLigne, column=1, columnspan=2, sticky=E+W)
        vLigne += 1
        Label (vFen, text="Degr� d'Urgence : ").grid(row=vLigne, column=0, sticky=W )
        self.cbDegUrg = Commun.comboWidget (self.root, vFen, self.root.cfgListe['DegUrgOBNT'])
        self.cbDegUrg.grid (row=vLigne, column=1, columnspan=2, sticky = W)
        vLigne += 1

        Label (vFen, text="Corps du message ", fg="blue",bg="cyan" ).grid(row= vLigne, column=0,columnspan=6, sticky=E+W)
        vLigne += 1
        Label (vFen, text="Objet : ").grid(row= vLigne, column=0, sticky=W)
        self.efObjet = Pmw.EntryField (vFen, validate=Commun.nonVideValidator)
        self.efObjet.grid (row= vLigne, column=1, columnspan=3, sticky=E+W)
        vLigne += 1
        Label (vFen, text="R�f�rence : ").grid(row=vLigne, column=0, sticky=W)
        self.eRef = Entry (vFen)
        self.eRef.grid (row= vLigne, column=1, columnspan=2, sticky=E+W)
        vLigne += 1
        Label (vFen, text="Message : ").grid(row=vLigne, column=0, sticky=W)
        self.stMessage = ScrolledText (vFen, wrap="word", height=12)
        self.stMessage.grid (row=vLigne, column=1, columnspan=4, sticky=E+W)
        vLigne += 12

        Label (vFen,text="Final du message ", fg="blue",bg="cyan").grid(row=vLigne, column=0, columnspan=6, sticky=E+W)
        vLigne += 1
        Label (vFen, text="GDH D�p�t/R�daction : ").grid(row=vLigne, column=0, sticky=W )
        self.efGdhDep = Commun.gdhWidget(vFen, vFen)
        self.efGdhDep.grid (row=vLigne, column=1, sticky=W)
        self.rbACK = Pmw.RadioSelect(vFen, buttontype="radiobutton",labelpos=W,label_text="Demande Accus� de R�ception : ")
        self.rbACK.grid(row=vLigne, column=3, columnspan=2, sticky=W)
        self.rbACK.add("Oui")
        self.rbACK.add("Non")
        vLigne += 1
      
        Label (vFen,text="Fin de Message ", fg="blue",bg="orange").grid(row=vLigne, column=0, columnspan=8, sticky=E+W)
        vLigne += 1

        Button (vFen, text="Valider", command = self.validerOBNT, fg="red", underline = 0).grid(row=vLigne, column=0, padx=5, pady=5, sticky=E+W)
        Button (vFen, text="Annuler", command = self.annulerOBNT, fg="red", underline = 1).grid(row=vLigne, column=2, padx=5, pady=5, sticky=E+W)
        Button (vFen, text="Quitter", command = self.quitterOBNT, fg="red", underline = 0).grid(row=vLigne, column=4, padx=5, pady=5, sticky=E+W)


    # D�finition des bulles d'aide sur la fen�tre
    def bulleAide(self):
        # ATTENTION, les message d'aide des Widgets GesADRA sont d�j� g�r�s
        self.fenetre.bulle.bind(self.stMessage, "Texte du message, sur plusieurs lignes si besoin")


    # Action sur un bouton "Valider"
    def validerOBNT(self, evt = None):
        "Traitement du bouton 'Valider'"

        #Contr�le de la validit� des donn�es
        if self.controleSaisie() == False:
            # Si erreur, on stoppe le traitement
            return None

        # Recalcul des donn�es variables (Gdh, N� message, etc...)
        if self.iGdh.get() == True :
            self.efGdh.setvalue("")
            vGdh=datetime.datetime.now().strftime("%d/%m/%y %H:%M")
            self.efGdh.setvalue(vGdh)
            
        # R�daction du message
        self.redigerOBNT()

        # Impression
        if self.root.userData['IMPR_MSG'] == "OUI" :
            os.startfile(Commun.getFullPath(self.root, self.vFicOBNT+".TXT"), "print")
        else :
            tkMessageBox.showinfo('Message OBNT', 'Message cr�� : ' + self.vFicOBNT)

        self.fenetre.destroy()

        
    # Action sur le bouton "Annuler"
    def annulerOBNT(self, evt = None):
        "Traitement du bouton 'Annuler'"
        # Remise � Z�ro de la saisie
        self.razSaisie()


    # Action sur le bouton "Quitter"
    def quitterOBNT(self, evt = None):
        "Traitement du bouton 'Quitter'"
        etesVousSur = tkMessageBox.askquestion("Fermeture du Formulaire", \
                                               "Confirmez-vous la fermeture du Message OBNT ?")
        if etesVousSur == "yes" :
            self.fenetre.destroy()
        else:
            self.fenetre.focus_set()


    # Traitement du bind <Return> sp�cifique
    def notReturn (self, evt = None):
        """Reproduire le comportement normal de la touche <Entr�e> pour un ScrolledText"""
        self.stMessage.insert(self.stMessage.index(INSERT), "\n")
        return "break"
        

    # Remise � z�ro de la saisie utilisateur
    def razSaisie(self):
        vGdh=datetime.datetime.now().strftime("%d/%m/%y %H:%M")
        self.efGdh.setvalue(vGdh) # Gdh transmission
        self.ckGdh.select() # Cocher pour recalculer le Gdh
        self.cbEmetteur.setentry("")
        self.cbDestinataire.setentry("")
        self.eInstruc.delete(0,END)
        self.efOrigine.setvalue("")
        self.efDestAction.setvalue("")
        self.eDestInfo.delete(0, END)
        self.cbDegUrg.selectitem(self.root.userData['URG_OBNT'])
        self.efObjet.setvalue("")
        self.eRef.delete(0, END)
        self.stMessage.delete(1.0,END)
        self.efGdhDep.setvalue(vGdh) # Gdh r�daction message
        self.rbACK.invoke("Non") # Demande Ack


    # Validation de la saisie utilisateur
    def controleSaisie(self):
        #Contr�le de saisie
        if not (self.efGdh.valid() and self.cbEmetteur.valid() and self.cbDestinataire.valid() and \
                self.efOrigine.valid() and self.efDestAction.valid()and self.efObjet.valid() and \
                self.efGdhDep.valid()):
            tkMessageBox.showwarning('Contr�le', 'Les champs en rouge sont absents ou incorrects')
            self.fenetre.focus_set()
            return False
       
        if self.stMessage.get(1.0, END).strip() == "":
            tkMessageBox.showwarning('Controle', 'Message vide')
            self.stMessage.focus_set()
            return False

        return True

        
    # Creation des fichiers message
    def redigerOBNT(self):

        # Nom du fichier
        self.vFicOBNT = Commun.getFicOBNT(self.root)
        # Fichier TXT
        self.txtFileOBNT()
        # Fichier XML
        self.xmlFileOBNT()
        
        # Ecriture d'une ligne dans la main courante
        vTexte = "Message " + self.vFicOBNT + \
		         " de " + self.efOrigine.getvalue() + " vers " +  self.efDestAction.getvalue()
        infosMCI = Commun.InfosMCI(self.efGdh.getvalue(), self.cbEmetteur.get(), self.cbDestinataire.get(), \
                                   self.cbDegUrg.get(), " ", vTexte)
        infosMCI.ecrire(self.root)
        
    
    def txtFileOBNT(self):
        
        fic = open(Commun.getFullPath(self.root, self.vFicOBNT+".TXT"),'w')
        
        fic.write(self.vFicOBNT+"\n\n")
        fic.write('################################################################################\n')
        fic.write('- ' +(self.root.userData['ACTIVATION'] + ' - ')*3+'\n')
        fic.write('--------------------------------------------------------------------------------\n')

        # Informations transmission
        fic.write("GDH Emission : " + self.efGdh.getvalue()+"\n")
        fic.write("Emis par     : " + self.cbEmetteur.get()+"\n")
        fic.write("Recu par     : " + self.cbDestinataire.get()+"\n")
        fic.write("Instructions : " + self.eInstruc.get()+"\n")
        fic.write('================================================================================\n')

        # Ent�te du message
        fic.write("MESSAGE OBNT".center(80) + "\n")
        fic.write("Origine      : " + self.efOrigine.getvalue()+"\n")
        fic.write("Dest. Action : " + self.efDestAction.getvalue()+"\n")
        fic.write("Dest. Info   : " + self.eDestInfo.get()+"\n")
        fic.write("Urgence      : " + self.cbDegUrg.get()+"\n")
        fic.write('--------------------------------------------------------------------------------\n')

        # Corps du message
        fic.write("Objet        : " + self.efObjet.get()+"\n")
        fic.write("R�f�rence    : " + self.eRef.get()+"\n")
        fic.write("Message : \n\n")
        # d�coupage des lignes du message
        for ligne in self.stMessage.get(1.0,END).split("\n"):
            if len(ligne) > 79:
                for ligne in textwrap.wrap(ligne,79):
                    fic.write(ligne +"\n")
            else:
               fic.write(ligne + "\n")
        fic.write('--------------------------------------------------------------------------------\n')

        # Final du message
        fic.write("GDH D�p�t    : " + self.efGdhDep.getvalue()+"\n")
        fic.write("Demande A.R. : " + self.rbACK.getvalue()+"\n")
        fic.write("FIN DE MESSAGE".center(80) + "\n")
        fic.write('================================================================================\n')
        fic.write('- ' +(self.root.userData['ACTIVATION'] + ' - ')*3+'\n')
        fic.write('################################################################################\n')

        fic.close()

    #
    def xmlFileOBNT(self):

        fic = open(Commun.getFullPath(self.root, self.vFicOBNT+".XML"),'w')
        
        fic.write('<?xml version="1.0" encoding="iso-8859-15"?><?xml-stylesheet type="text/xsl" href="..\msgOBNT.XSL"?>\n')
        fic.write('<msg>\n')
        fic.write('<form>Message OBNT</form>\n')
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
        fic.write("<obj>" + self.efObjet.getvalue()+"</obj>\n")
        fic.write("<ref>" + self.eRef.get()+"</ref>\n")
        # d�coupage des lignes du message
        for ligne in self.stMessage.get(1.0,END).split("\n"):
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
