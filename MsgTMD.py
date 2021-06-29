# -*- coding: iso-8859-15 -*-

from tkinter import *
from tkinter.scrolledtext import ScrolledText

import datetime
import time
import os
import tkinter.messagebox as tkMessageBox
import Pmw
import Commun # Module principal des fonctions annexes


###################### Creation d'un message TMD
class FormTMD:
    "Classe définissant le formulaire TMD"
    
    def __init__(self, appli):
        "Constructeur de la fenêtre TMD"

        self.root = appli # Référence à l'application racine
        self.emballage = [] # liste des lignes emballage

        # Création de la nouvelle fenêtre
        self.fenetre = Commun.nouvelleFenetre(self.root, "Message Transport de Matière Dangereuse")
        # Fermeture par la case système
        self.fenetre.protocol("WM_DELETE_WINDOW", self.quitterTMD)

        # Composants de la fenêtre
        self.dessineTMD()

        # Initialisations
        self.razSaisie()
        
        # Gestion des raccourcis clavier
        self.fenetre.bind('<Alt-v>', self.validerTMD)
        self.fenetre.bind('<Return>', self.validerTMD)
        self.fenetre.bind('<Alt-n>', self.annulerTMD)
        self.fenetre.bind('<Escape>', self.annulerTMD)
        self.fenetre.bind('<Alt-q>', self.quitterTMD)
        
        
    def dessineTMD(self):

        # variables locales
        vLigne = 1 # N° de ligne pour le positionnement des composants
        vFen = self.fenetre

        # Composants de la fenêtre
        Label (vFen,text = "Informations transmission", fg = "blue",bg = "orange").grid(row = vLigne, column = 0, columnspan = 9, sticky = W+E)
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
        Label (vFen, text = "Reçu par : ").grid(row = vLigne, column = 3, sticky = W)
        self.cbDestinataire = Commun.indicatifWidget(vFen, vFen, self.root)
        self.cbDestinataire.grid (row = vLigne, column = 4, sticky = W+E)
        vLigne += 1

        Label (vFen, text = "Instructions particulières : ").grid(row = vLigne, column = 0, sticky = W)
        self.eInstruc = Entry (vFen)
        self.eInstruc.grid (row = vLigne, column = 1, columnspan = 4, sticky = W+E)
        vLigne += 1

        Label (vFen, text = "Message Transport Matières Dangereuses", fg = "blue", bg = "orange").grid(row = vLigne, column = 0, columnspan = 9, sticky = W+E)
        vLigne += 1

        Label (vFen,text = "Entête du Message", fg = "blue", bg = "cyan").grid(row = vLigne, column = 0,columnspan = 9, sticky = E+W )
        vLigne += 1

        Label (vFen, text = "Origine : ").grid(row = vLigne, column = 0, sticky = W)
        self.efOrigine = Pmw.EntryField (vFen, validate = Commun.nonVideValidator)
        self.efOrigine.grid (row = vLigne, column = 1, sticky = W)
        vLigne += 1

        Label (vFen, text = "Destinataires Action : ").grid(row = vLigne, column = 0, sticky = W)
        self.efDestAction = Pmw.EntryField (vFen, validate = Commun.nonVideValidator)
        self.efDestAction.grid (row = vLigne, column = 1, columnspan = 3, sticky = W+E)
        Label (vFen, text = "(utilisez le / comme séparateur)").grid(row = vLigne, rowspan = 2, column = 4, columnspan = 5, sticky = W)
        vLigne += 1

        Label (vFen, text = "Destinataires Info : ").grid(row = vLigne, column = 0, sticky = W)
        self.eDestInfo = Entry(vFen)
        self.eDestInfo.grid (row = vLigne, column = 1, columnspan = 3, sticky = W+E)
        vLigne += 1

        Label (vFen, text = "Degré d'Urgence : ").grid(row = vLigne, column = 0, sticky = W)
        self.cbDegUrg = Commun.comboWidget (self.root, vFen, self.root.cfgListe['DegUrgOBNT'])
        self.cbDegUrg.grid (row = vLigne, column = 1, columnspan = 2, sticky = W)
        vLigne += 1

        Label (vFen,text = "Corps de message", fg = "blue",bg = "cyan").grid(row = vLigne , column = 0,columnspan = 9, sticky = E+W )
        vLigne += 1

        self.notebook = Pmw.NoteBook(vFen)
        self.notebook.grid(row = vLigne, column = 0, columnspan = 9, sticky = W+E)
        self.nbTab1 = self.notebook.add('Véhicule')
        vLig = 0
        Label (self.nbTab1, text = "Description du véhicule", fg = "blue",bg = "darkgrey").grid(row = vLig, column = 0, columnspan = 9, sticky = W+E)
        vLig += 1

        Label (self.nbTab1, text = "Véhicule : " ).grid(row = vLig, column = 0, sticky = W)
        self.cbVehicule = Commun.comboWidget (self.root, self.nbTab1, self.root.cfgListe['Vehicule'])
        self.cbVehicule.grid(row = vLig, column = 1, columnspan = 2, sticky = W+E)
        Label (self.nbTab1, text = "Type : " ).grid(row = vLig, column = 3, sticky = W)
        self.cbTypVeh = Commun.comboWidget (self.root, self.nbTab1, self.root.cfgListe['TypVeh'])
        self.cbTypVeh.grid (row = vLig, column = 4, columnspan = 2, sticky = W+E)
        Label (self.nbTab1, text = "Poids (T) : " ).grid(row = vLig, column = 6, sticky = W)
        self.ePoidsVeh = Entry (self.nbTab1)
        self.ePoidsVeh.grid (row = vLig,column = 7,sticky = E+W )
        vLig += 1

        Label (self.nbTab1, text = "Capacité (m3) : " ).grid(row = vLig, column = 0, sticky = W)
        self.eCapCit = Entry (self.nbTab1)
        self.eCapCit.grid (row = vLig,column = 1,sticky = W)
        Label (self.nbTab1, text = "Volume du Fret (m3) : " ).grid(row = vLig, column = 3, sticky = W)
        self.eVolMat = Entry (self.nbTab1)
        self.eVolMat.grid (row = vLig,column = 4,sticky = W)
        Label (self.nbTab1, text = "Poids du Fret (T) : " ).grid(row = vLig, column = 6, sticky = W)
        self.ePoidsFret = Entry (self.nbTab1)
        self.ePoidsFret.grid (row = vLig,column = 7,sticky = W)
        vLig += 1

        Label (self.nbTab1, text = "Nb compartiments calorifugés : " ).grid(row = vLig, column = 0, sticky = W)
        self.eCompart = Entry (self.nbTab1)
        self.eCompart.grid (row = vLig,column = 1,sticky = W)
        Label (self.nbTab1, text = "Syst. de réchauffage : " ).grid(row = vLig, column = 3, sticky = W)
        self.eRechauf = Entry (self.nbTab1)
        self.eRechauf.grid (row = vLig,column = 4,sticky = W)
        Label (self.nbTab1, text = "Syst. refrigérant : " ).grid(row = vLig, column = 6, sticky = W)
        self.eRefrig = Entry (self.nbTab1)
        self.eRefrig.grid (row = vLig,column = 7,sticky = W)
        vLig += 1

        self.nbTab2 = self.notebook.add('Fret')
        self.nbTab2.grid_columnconfigure(0, weight=2)
        self.nbTab2.grid_columnconfigure(9, weight=2)
        vLig = 0
        Label (self.nbTab2, text = "Conditionnement du Fret", fg = "blue",bg = "darkgrey").grid(row = vLig, column = 0,columnspan = 11, sticky = W+E)
        vLig += 1
        Label (self.nbTab2, text = "Conditionnement" ).grid(row = vLig, column = 2, sticky = W)
        Label (self.nbTab2, text = "Nombre" ).grid(row = vLig, column = 4, sticky = W)
        Label (self.nbTab2, text = "Poids ou Volume" ).grid(row = vLig, column = 5, sticky = W)
        vLig += 1
        self.cbCond = Commun.comboWidget (self.root, self.nbTab2, self.root.cfgListe['Cond'])
        self.cbCond.grid(row = vLig, column = 2, sticky = W)
        self.eNbCond = Entry (self.nbTab2)
        self.eNbCond.grid(row = vLig, column = 4, sticky = W)
        self.ePoidsCond = Entry (self.nbTab2)
        self.ePoidsCond.grid(row = vLig, column = 5, sticky = W)
        vLig += 1

        Label (self.nbTab2, text = "Sous-Emballage" ).grid(row = vLig, column = 1, sticky = W)
        Label (self.nbTab2, text = "Matiere" ).grid(row = vLig, column = 2, sticky = W)
        Label (self.nbTab2, text = "Quantité" ).grid(row = vLig, column = 4, sticky = W)
        Label (self.nbTab2, text = "Poids ou Volume" ).grid(row = vLig, column = 5, sticky = W)
        vLig += 1
        for i in range(4):
            cbRecipient = Commun.comboWidget (self.root, self.nbTab2, self.root.cfgListe['Recipient'])
            cbRecipient.grid (row = vLig + i, column = 1, sticky = W)
            cbMatiereSac = Commun.comboWidget (self.root, self.nbTab2, self.root.cfgListe['Matiere'])
            cbMatiereSac.grid (row = vLig + i, column = 2,sticky = W)
            efQte = Pmw.EntryField (self.nbTab2)
            efQte.grid (row = vLig + i, column = 4, sticky = W)
            efPoids = Pmw.EntryField (self.nbTab2)
            efPoids.grid (row = vLig + i, column = 5, sticky = W)
            self.emballage.append((cbRecipient,cbMatiereSac,efQte,efPoids))
            # Masquer des comboBox jusqu'au setnaturalsize pour pbm d'affichage
            cbRecipient.grid_remove() 
            cbMatiereSac.grid_remove()
        
        self.nbTab3 = self.notebook.add('Transporteur')
        self.nbTab3.grid_columnconfigure(0, weight=2)
        self.nbTab3.grid_columnconfigure(9, weight=2)
        vLig = 0
        Label (self.nbTab3, text = "Identification du Transporteur", fg = "blue",bg = "darkgrey").grid(row = vLig, column = 0,columnspan = 11, sticky = W+E)
        vLig += 1
        Label (self.nbTab3, text = "Nom : " ).grid(row = vLig, column = 0, sticky = W)
        self.eNom = Entry (self.nbTab3)
        self.eNom.grid (row = vLig, column = 1, columnspan = 3, sticky = W+E)
        Label (self.nbTab3, text = "Tel/Fax : " ).grid(row = vLig, column = 4, sticky = W)
        self.eTel = Entry (self.nbTab3)
        self.eTel.grid (row = vLig,column = 6,sticky = W)
        vLig += 1

        Label (self.nbTab3, text = "Adresse : " ).grid(row = vLig, column = 0, sticky = W)
        self.eAdr = Entry (self.nbTab3)
        self.eAdr.grid (row = vLig, column = 1 ,columnspan = 6, sticky = E+W)
        vLig += 1

        Label (self.nbTab3, text = "Immat. véhicule : " ).grid(row = vLig, column = 0, sticky = W)
        self.eImmat = Entry (self.nbTab3)
        self.eImmat.grid (row = vLig,column = 1,sticky = W)
        Label (self.nbTab3, text = "Nationalité : " ).grid(row = vLig, column = 4, sticky = W)
        self.eNation = Entry (self.nbTab3)
        self.eNation.grid (row = vLig, column = 6, sticky = W)
        vLig += 1

        Label (self.nbTab3, text = "Expéditeur Fret : " ).grid(row = vLig, column = 0, sticky = W)
        self.eExped = Entry (self.nbTab3)
        self.eExped.grid (row = vLig, column = 1, columnspan = 3, sticky = W+E)
        Label (self.nbTab3, text = "Destinataire Fret : " ).grid(row = vLig, column = 4, sticky = W)
        self.eClient = Entry (self.nbTab3)
        self.eClient.grid (row = vLig, column = 6, columnspan = 2, sticky = W+E)
        vLig += 1
    
        self.notebook.setnaturalsize()
        # Afficher des comboBox itératives après le setnaturalsize pour pbm d'affichage
        for ligne in self.emballage: 
            ligne[0].grid()
            ligne[1].grid()
        vLigne += 6
        Label (vFen, text = "Final du message ", fg = "blue",bg = "cyan").grid(row = vLigne, column = 0, columnspan = 9, sticky = E+W)
        vLigne += 1
        Label (vFen, text = "GDH Dépôt/Rédaction : ").grid(row = vLigne, column = 0, sticky = W)
        self.efGdhDep = Commun.gdhWidget(vFen, vFen)
        self.efGdhDep.grid (row = vLigne, column = 1, sticky = W)
        self.rbACK = Pmw.RadioSelect(vFen, buttontype = "radiobutton",labelpos = W,label_text = "Demande Accusé de Réception : ")
        self.rbACK.grid(row = vLigne, column = 4, columnspan = 4, sticky = W)
        self.rbACK.add("Oui")
        self.rbACK.add("Non")
        vLigne += 1
        
        Label (vFen,text = "Fin de message", fg = "blue",bg = "orange").grid(row = vLigne, column = 0,columnspan = 9, sticky = E+W )
        vLigne += 1
        Button (vFen, text = "Valider", command = self.validerTMD, fg = "red", underline = 0).grid(row = vLigne, column = 1, padx = 5, pady = 5, sticky = W+E)
        Button (vFen, text = "Annuler", command = self.annulerTMD, fg = "red", underline = 1).grid(row = vLigne, column = 4, padx = 5, pady = 5, sticky = W+E)
        Button (vFen, text = "Quitter", command = self.quitterTMD, fg = "red", underline = 0).grid(row = vLigne, column = 6, padx = 5, pady = 5, sticky = W+E)


    # Action sur un bouton "Valider"
    def validerTMD(self, evt = None):
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
        self.redigerTMD()

        # Impression
        if self.root.userData['IMPR_MSG'] == "OUI" :
            os.startfile(Commun.getFullPath(self.root, self.vFicTMD+".TXT"), "print")
        else :
            tkMessageBox.showinfo('Message TMD', 'Message créé : ' + self.vFicTMD)
        
	# self.fenetre.destroy


    # Action sur un bouton "Annuler"
    def annulerTMD(self, evt = None):
        self.razSaisie()
        

    # Action sur un bouton "Quitter"
    def quitterTMD(self, evt = None):
        "Traitement du bouton 'Quitter'"
        etesVousSur = tkMessageBox.askquestion("Fermeture du Formulaire", \
                                               "Confirmez-vous la fermeture du Message TMD ?")
        if etesVousSur == "yes" :
            self.fenetre.destroy()
        else:
            self.fenetre.focus_set()


    # Validation de la saisie utilisateur
    def controleSaisie(self):
        if not (self.efGdh.valid() and self.cbEmetteur.valid() and self.cbDestinataire.valid() and \
                self.efOrigine.valid() and self.efDestAction.valid()):
            tkMessageBox.showwarning('Contrôle', 'Les champs en rouge sont absents ou incorrects')
            self.fenetre.focus_set()
            return False

        return True


    # Remise à zéro de la saisie utilisateur
    def razSaisie(self):
        vGdh = datetime.datetime.now().strftime("%d/%m/%y %H:%M")
        self.efGdh.setvalue(vGdh) # Gdh transmission
        self.ckGdh.select() # Cocher pour recalculer le Gdh
        self.cbEmetteur.setentry("")
        self.cbDestinataire.setentry("")
        self.eInstruc.delete(0,END)
        self.efOrigine.setvalue("")
        self.efDestAction.setvalue("")
        self.eDestInfo.delete(0, END)
        self.cbDegUrg.selectitem(self.root.userData['URG_TMD'])
        self.cbVehicule.setentry("")
        self.cbTypVeh.setentry("")
        self.ePoidsVeh.delete(0,END)
        self.eCapCit.delete(0, END)
        self.eVolMat.delete(0, END)
        self.ePoidsFret.delete(0, END)
        self.eCompart.delete(0, END)
        self.eRechauf.delete(0, END)
        self.eRefrig.delete(0, END)
        self.cbCond.setentry("")
        self.eNbCond.delete(0, END)
        self.ePoidsCond.delete(0, END)
        for ligne in self.emballage: 
            ligne[0].setentry("")
            ligne[1].setentry("")
            ligne[2].setentry("")
            ligne[3].setentry("")
        self.eNom.delete(0, END)
        self.eTel.delete(0, END)
        self.eAdr.delete(0, END)
        self.eImmat.delete(0, END)
        self.eNation.delete(0, END)
        self.eExped.delete(0, END)
        self.eClient.delete(0, END)
        self.efGdhDep.setvalue(vGdh)
        self.rbACK.invoke("Non") # Demande Ack


    # Creation des fichiers message
    def redigerTMD(self):

        # Nom du fichier
        self.vFicTMD = Commun.getFicTMD(self.root)
        # Fichier TXT
        self.txtFileTMD()
        # Fichier XML
        self.xmlFileTMD()
        
        # Ecriture d'une ligne dans la main courante
        vTexte = "Message " + self.vFicTMD + \
		         " de " + self.efOrigine.getvalue() + " vers " +  self.efDestAction.getvalue()
        infosMCI = Commun.InfosMCI(self.efGdh.getvalue(), self.cbEmetteur.get(), self.cbDestinataire.get(), \
                                   self.cbDegUrg.get(), " ", vTexte)
        infosMCI.ecrire(self.root)
        
    
    def txtFileTMD(self):
        
        fic = open(Commun.getFullPath(self.root, self.vFicTMD+".TXT"),'w')
        
        fic.write(self.vFicTMD+"\n\n")
        fic.write('################################################################################\n')
        fic.write('- ' +(self.root.userData['ACTIVATION'] + ' - ')*3+'\n')
        fic.write('--------------------------------------------------------------------------------\n')
    
        # Informations transmission
        fic.write("GDH Emission : " + self.efGdh.getvalue()+ "\n")
        fic.write("Emis par     : " + self.cbEmetteur.get()+ "\n")
        fic.write("Reçu par     : " + self.cbDestinataire.get()+ "\n")
        fic.write("Instructions : " + self.eInstruc.get()+ "\n")
        fic.write('================================================================================\n')

        # Entête du message
        fic.write("MESSAGE TRANSPORT MATIERES DANGEUREUSES".center(80) + "\n")
        fic.write("Origine      : " + self.efOrigine.getvalue()+"\n")
        fic.write("Dest. Action : " + self.efDestAction.getvalue()+"\n")
        fic.write("Dest. Info   : " + self.eDestInfo.get()+"\n")
        fic.write("Urgence      : " + self.cbDegUrg.get()+"\n")
        fic.write('--------------------------------------------------------------------------------\n')

        # Description véhicule
        fic.write("Véhicule            : " + self.cbVehicule.get()+"\n")
        fic.write("Type                : " + self.cbTypVeh.get()+"\n")
        fic.write("Poids (T)           : " + self.ePoidsVeh.get()+"\n")
        fic.write("Capacité (m3)       : " + self.eCapCit.get()+"\n")
        fic.write("Volume du Fret (m3) : " + self.eVolMat.get()+"\n")
        fic.write("Poids du Fret (T)   : " + self.ePoidsFret.get()+"\n")
        fic.write("Nb compartiments calorifugés : "  + self.eCompart.get()+"\n")
        fic.write("Syst. réchauffage   : " + self.eRechauf.get()+"\n")
        fic.write("Syst. refrigérant   : " + self.eRefrig.get()+"\n")
        fic.write('--------------------------------------------------------------------------------\n')

        #   
        fic.write("Conditionnement : " + self.cbCond.get()+"\n")
        fic.write("Nombre          : " + self.eNbCond.get()+"\n")
        fic.write("Poids ou Volume : " + self.ePoidsCond.get()+"\n")
        fic.write("\n")
        fic.write (" Sous-emballage    Matiere       Quantite    Poids ou Volume\n")
        for ligne in self.emballage : 
            try:
                fic.write (ligne[0].get().center(15))
                fic.write (ligne[1].get().center(15))
                fic.write (ligne[2].getvalue().center(15))
                fic.write (ligne[3].getvalue().center(15) + "\n")
            except:
                None
        fic.write('--------------------------------------------------------------------------------\n')

        # Identité du Transporteur et du Véhicule
        fic.write("Nom          : " + self.eNom.get()+"\n")
        fic.write("Tel/Fax      : " + self.eTel.get()+"\n")
        fic.write("Adresse      : " + self.eAdr.get()+"\n")
        fic.write("Immat. véh.  : " + self.eImmat.get()+"\n")
        fic.write("Nationalité  : " + self.eNation.get()+"\n")
        fic.write("Expéd. Fret  : " + self.eExped.get()+"\n")
        fic.write("Destin. Fret : " + self.eClient.get()+"\n")
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
    def xmlFileTMD(self):

        fic = open(Commun.getFullPath(self.root, self.vFicTMD+".XML"),'w')
        
        fic.write('<?xml version="1.0" encoding="iso-8859-15"?><?xml-stylesheet type="text/xsl" href="..\msgTMD.XSL"?>\n')
        fic.write('<msg>\n')
        fic.write('<form>Message TMD</form>\n')
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
          
        # Description véhicule
        fic.write("<ong1>\n")
        fic.write("<veh>" + self.cbVehicule.get()+"</veh>\n")
        fic.write("<type>" + self.cbTypVeh.get()+"</type>\n")
        fic.write("<pveh>" + self.ePoidsVeh.get()+"</pveh>\n")
        fic.write("<capa>" + self.eCapCit.get()+"</capa>\n")
        fic.write("<vfret>" + self.eVolMat.get()+"</vfret>\n")
        fic.write("<pfret>" + self.ePoidsFret.get()+"</pfret>\n")
        fic.write("<compart>"  + self.eCompart.get()+"</compart>\n")
        fic.write("<rechauf>" + self.eRechauf.get()+"</rechauf>\n")
        fic.write("<refrig>" + self.eRefrig.get()+"</refrig>\n")
        fic.write("</ong1>\n")
        fic.write("<ong2>\n")
        fic.write("<cond>" + self.cbCond.get()+"</cond>\n")
        fic.write("<nbcond>" + self.eNbCond.get()+"</nbcond>\n")
        fic.write("<poids>" + self.ePoidsCond.get()+"</poids>\n")
        for ligne in self.emballage : 
            if ligne[0].get().strip() != "":
                fic.write ("<emb>")
                fic.write ("<ssemb>" + ligne[0].get().center(15) +"</ssemb>\n")
                fic.write ("<mat>"   + ligne[1].get().center(15) + "</mat>\n") 
                fic.write ("<qte>"   + ligne[2].getvalue().center(15) + "</qte>\n")
                fic.write ("<pov>"   + ligne[3].getvalue().center(15) + "</pov>\n")
                fic.write ("</emb>")
        fic.write("</ong2>\n")
        fic.write("<ong3>\n")
        fic.write("<nom>" + self.eNom.get()+"</nom>\n")
        fic.write("<tel>" + self.eTel.get()+"</tel>\n")
        fic.write("<adr>" + self.eAdr.get()+"</adr>\n")
        fic.write("<immat>" + self.eImmat.get()+"</immat>\n")
        fic.write("<nation>" + self.eNation.get()+"</nation>\n")
        fic.write("<exped>" + self.eExped.get()+"</exped>\n")
        fic.write("<client>" + self.eClient.get()+"</client>\n")
        fic.write("</ong3>\n")
        fic.write('</corps>\n')
        fic.write('<bot>\n')
        fic.write("<gdh>" + self.efGdhDep.getvalue()+"</gdh>\n")
        fic.write("<ack>" + self.rbACK.getvalue()+"</ack>\n")
        fic.write('</bot>\n')
            
        fic.write('</msg>\n')
    
        fic.close()
    #
          
          