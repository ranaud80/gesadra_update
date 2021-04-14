# -*- coding: iso-8859-15 -*-

from Tkinter import *
from ScrolledText import ScrolledText
 
import datetime
import time
import os
import tkMessageBox
import tkFont
import Pmw
import Commun # Module principal des fonctions annexes

###################### Creation d'un message Bilan Temporaire.
class FormBT:
    "Classe d�finissant le formulaire Bilan Temporaire"
    
    def __init__(self, appli):
        "Constructeur de la fen�tre BT"

        self.root = appli # R�f�rence � l'application racine

        # Cr�ation de la nouvelle fen�tre
        self.fenetre = Commun.nouvelleFenetre(self.root, "Message de Bilan Temporaire")
        # Fermeture par la case syst�me
        self.fenetre.protocol("WM_DELETE_WINDOW", self.quitterBT)
        
        # Composants de la fen�tre
        self.dessineBT()

        # Initialisations
        self.razSaisie()
        
        # Gestion des raccourcis clavier
        self.fenetre.bind('<Alt-v>', self.validerBT)
        self.fenetre.bind('<Return>', self.validerBT)
        self.fenetre.bind('<Alt-n>', self.annulerBT)
        self.fenetre.bind('<Escape>', self.annulerBT)
        self.fenetre.bind('<Alt-q>', self.quitterBT)
        

    def dessineBT(self):

        # variables locales
        vLigne = 1 # N� de ligne pour le positionnement des composants
        vNomBouton = ""
        vIndice = 0
        vFen = self.fenetre

        # Composants de la fen�tre
        Label (vFen,text = "Informations transmission", fg = "blue",bg = "orange").grid(row = vLigne, column = 0, columnspan = 8, sticky = W+E)
        vLigne += 1

        Label (vFen, text = "Groupe Date/Heure : ").grid(row = vLigne, column = 0, sticky = W)
        self.efGdh = Commun.gdhWidget(vFen, vFen)
        self.efGdh.grid(row = vLigne, column = 1, sticky = W)
        self.iGdh = IntVar()
        self.ckGdh = Checkbutton (vFen, text = "Recalculer le GDH lors de la validation", variable = self.iGdh)
        self.ckGdh.grid(row = vLigne, column = 3, columnspan = 2, sticky = W)
        self.ckGdh.select()
        vLigne += 1
        Label (vFen, text = "Emis par : ").grid(row = vLigne, column = 0, sticky = W)
        self.cbEmetteur = Commun.indicatifWidget(vFen, vFen, self.root)
        self.cbEmetteur.grid (row = vLigne, column = 1, sticky = W)
        Label (vFen, text = "Re�u par : ").grid(row = vLigne, column = 3, sticky = W)
        self.cbDestinataire = Commun.indicatifWidget(vFen, vFen, self.root)
        self.cbDestinataire.grid (row = vLigne, column = 4, columnspan = 4, sticky = W)
        vLigne += 1
        Label (vFen, text = "Instructions particuli�res : ").grid(row = vLigne, column = 0, sticky = W)
        self.eInstruc = Entry (vFen)
        self.eInstruc.grid (row = vLigne, column = 1, columnspan = 4, sticky = W+E)
        vLigne += 1

        Label (vFen,text = "Message Bilan Temporaire", fg = "blue",bg = "orange").grid(row = vLigne, column = 0, columnspan = 8, sticky = W+E)
        vLigne += 1

        Label (vFen,text = "Ent�te du Message", fg = "blue",bg = "cyan").grid(row = vLigne, column = 0, columnspan = 8, sticky = W+E)
        vLigne += 1

        Label (vFen, text = "Origine : ").grid(row = vLigne, column = 0, sticky = W)
        self.efOrigine = Pmw.EntryField (vFen, validate = Commun.nonVideValidator)
        self.efOrigine.grid (row = vLigne, column = 1, sticky = W)
        vLigne += 1
        Label (vFen, text = "Destinataires Action: ").grid(row = vLigne, column = 0, sticky = W)
        self.efDestAction = Pmw.EntryField (vFen, validate = Commun.nonVideValidator)
        self.efDestAction.grid (row = vLigne, column = 1, columnspan = 4, sticky = W+E)
        Label (vFen, text = "(utilisez le / comme s�parateur)").grid(row = vLigne, rowspan = 2, column = 5, columnspan = 3, sticky = W)
        vLigne += 1
        Label (vFen, text = "Destinataires Info: ").grid(row = vLigne, column = 0, sticky = W)
        self.eDestInfo = Entry(vFen)
        self.eDestInfo.grid (row = vLigne, column = 1, columnspan = 4, sticky = W+E)
        vLigne += 1
        Label (vFen, text = "Degr� d'Urgence : ").grid(row = vLigne, column = 0, sticky = W)
        self.cbDegUrg = Commun.comboWidget (self.root, vFen, self.root.cfgListe['DegUrgOBNT'])
        self.cbDegUrg.grid (row = vLigne, column = 1, columnspan = 2, sticky = W)
        vLigne += 1

        Label (vFen, text = "Corps du message ", fg = "blue",bg = "cyan").grid(row = vLigne, column = 0,columnspan = 8, sticky = W+E)
        vLigne += 1

        Label (vFen, text = "Objet : ").grid(row = vLigne, column = 0, sticky = W)
        self.efObjet = Pmw.EntryField (vFen, validate = Commun.nonVideValidator)
        self.efObjet.grid (row = vLigne, column = 1, columnspan = 6, sticky = W+E)
        vLigne += 1
        Label (vFen, text = "D�pt. Alert� et Touch� : ").grid(row = vLigne, column = 0, sticky = W)
        self.eDptAET = Entry (vFen)
        self.eDptAET.grid (row = vLigne, column = 1, sticky = W)
        Label (vFen, text = "D�pt. Touch� et Non Alert� : ").grid(row = vLigne, column = 3, sticky = W)
        self.eDptTNA = Entry (vFen)
        self.eDptTNA.grid (row = vLigne, column = 4, sticky = W)
        Label (vFen, text = "Dept. Alert� et Non Touch� : ").grid(row = vLigne, column = 6, sticky = W)
        self.eDptANT = Entry (vFen)
        self.eDptANT.grid (row = vLigne, column = 7, sticky = W)
        vLigne += 1

        Label (vFen, text = "Plan ORSEC : ").grid(row = vLigne, column = 0, sticky = W)
        self.cbORSEC = Pmw.ComboBox (vFen, scrolledlist_items = self.root.cfgListe['Orsec'], listheight = 80)
        self.cbORSEC.grid (row = vLigne, column = 1, columnspan = 2, sticky = W)
        self.cbORSEC.selectitem(0)

        Label (vFen, text = "Port�e ORSEC : ").grid(row = vLigne, column = 3, sticky = W)
        self.cbPortee = Pmw.ComboBox (vFen, scrolledlist_items = self.root.cfgListe['Portee'], listheight = 80)
        self.cbPortee.grid (row = vLigne, column = 4, columnspan = 2, sticky = W)
        self.cbPortee.selectitem(0)
        self.rbCrise = Pmw.RadioSelect(vFen, buttontype = "radiobutton",labelpos = W,label_text = "Cellule de Crise activ�e : ")
        self.rbCrise.grid(row = vLigne, column = 6, columnspan = 2, sticky = W)
        self.rbCrise.add("Oui")
        self.rbCrise.add("Non")
        self.rbCrise.invoke("Non")
        vLigne += 1
        
        self.notebook = Pmw.NoteBook(vFen)
        self.notebook.grid(row = vLigne, column = 0, columnspan = 8, sticky = W+E)
        self.nbTab1 = self.notebook.add('Bilan')
        self.nbTab1.grid_columnconfigure(1, weight=2)  
        self.nbTab1.grid_columnconfigure(4, weight=2)  
        self.nbTab1.grid_columnconfigure(7, weight=2)  
        self.nbTab1.grid_columnconfigure(8, weight=2)  
        vLig = 0
        Label (self.nbTab1,text = "Bilans Humain et Mat�riel", fg = "blue",bg = "darkgray").grid(row = vLig, column = 0,columnspan = 9, sticky = W+E)
        vLig += 1
        
        Label (self.nbTab1, text = "Nb D�c�d�s : ").grid(row = vLig, column = 0, sticky = W)
        self.eDecedes = Entry (self.nbTab1)
        self.eDecedes.grid (row = vLig, column = 1, sticky = W)
        Label (self.nbTab1, text = "Nb Bless�s : ").grid(row = vLig, column = 3, sticky = W)
        self.eBlesses = Entry (self.nbTab1)
        self.eBlesses.grid (row = vLig, column = 4, sticky = W)
        Label (self.nbTab1, text = "Nb D�plac�s ou Relog�s : ").grid(row = vLig, column = 6, sticky = W)
        self.eDeplaces = Entry (self.nbTab1)
        self.eDeplaces.grid (row = vLig, column = 7, sticky = W)
        vLig += 1

        Label (self.nbTab1, text = "Nb d'interventions : ").grid(row = vLig, column = 0, sticky = W)
        self.eInterv = Entry (self.nbTab1)
        self.eInterv.grid (row = vLig, column = 1, sticky = W)
        Label (self.nbTab1, text = "H�litreuill�s : ").grid(row = vLig, column = 3, sticky = W)
        self.eHeli = Entry (self.nbTab1)
        self.eHeli.grid (row = vLig, column = 4, sticky = W)
        Label (self.nbTab1, text = "Axe coup�s : ").grid(row = vLig, column = 6, sticky = W)
        self.eAxes = Entry (self.nbTab1)
        self.eAxes.grid (row = vLig, column = 7, sticky = W)
        vLig += 1

        Label (self.nbTab1, text = "Foyers Priv�s d'Eau : ").grid(row = vLig, column = 0, sticky = W)
        self.eSansEau = Entry (self.nbTab1)
        self.eSansEau.grid (row = vLig, column = 1, sticky = W)
        Label (self.nbTab1, text = "Foyers Priv�s Electricit� : ").grid(row = vLig, column = 3, sticky = W)
        self.eSansElec = Entry (self.nbTab1)
        self.eSansElec.grid (row = vLig, column = 4, sticky = W)
        Label (self.nbTab1, text = "Foyers Priv�s Telephone : ").grid(row = vLig, column = 6, sticky = W)
        self.eSansTel = Entry (self.nbTab1)
        self.eSansTel.grid (row = vLig, column = 7, sticky = W)
        vLig += 1

        self.nbTab2 = self.notebook.add('Effectifs')
        self.nbTab2.grid_columnconfigure(1, weight=2)  
        self.nbTab2.grid_columnconfigure(4, weight=2)  
        self.nbTab2.grid_columnconfigure(7, weight=2)  
        self.nbTab2.grid_columnconfigure(8, weight=2)  
        vLig = 0
        Label (self.nbTab2, text = "Effectifs Engag�s", fg = "blue",bg = "darkgray").grid(row = vLig, column = 0, columnspan = 9, sticky = W+E)
        vLig += 1

        Label (self.nbTab2, text = "SP Locaux : ").grid(row = vLig, column = 0, sticky = W)
        self.eSPLoc = Entry (self.nbTab2)
        self.eSPLoc.grid (row = vLig, column = 1, sticky = W)
        Label (self.nbTab2, text = "SP Extra zonaux : ").grid(row = vLig, column = 3, sticky = W)
        self.eSPExt = Entry (self.nbTab2)
        self.eSPExt.grid (row = vLig, column = 4, sticky = W)
        Label (self.nbTab2, text = "Militaires S�curit� Civile : ").grid(row = vLig, column = 6, sticky = W)
        self.eMilSC = Entry (self.nbTab2)
        self.eMilSC.grid (row = vLig, column = 7, sticky = W)
        vLig += 1
        
        Label (self.nbTab2, text = "Police/Gendarmerie : ").grid(row = vLig, column = 0, sticky = W)
        self.ePolice = Entry (self.nbTab2)
        self.ePolice.grid (row = vLig, column = 1, sticky = W)
        Label (self.nbTab2, text = "Militaires : ").grid(row = vLig, column = 3, sticky = W)
        self.eArmee = Entry (self.nbTab2)
        self.eArmee.grid (row = vLig, column = 4, sticky = W)
        Label (self.nbTab2, text = "Asso. S�curit� Civile: ").grid(row = vLig, column = 6, sticky = W)
        self.eAssoSC = Entry(self.nbTab2)
        self.eAssoSC.grid (row = vLig, column = 7, sticky = W)
        vLig += 1
        
        Label (self.nbTab2, text = "EDF / GDF : ").grid(row = vLig, column = 0, sticky = W)
        self.eElec = Entry (self.nbTab2)
        self.eElec.grid (row = vLig, column = 1, sticky = W)
        Label (self.nbTab2, text = "France T�lecom : ").grid(row = vLig, column = 3, sticky = W)
        self.eTelecom = Entry (self.nbTab2)
        self.eTelecom.grid (row = vLig, column = 4, sticky = W)
        Label (self.nbTab2, text = "DDE/DIR/CG : ").grid(row = vLig, column = 6, sticky = W)
        self.eEquip = Entry (self.nbTab2)
        self.eEquip.grid (row = vLig, column = 7, sticky = W)
        vLig += 1

        self.nbTab3 = self.notebook.add('Moyens')
        self.nbTab3.grid_columnconfigure(1, weight=2)  
        self.nbTab3.grid_columnconfigure(4, weight=2)  
        self.nbTab3.grid_columnconfigure(7, weight=2)  
        self.nbTab3.grid_columnconfigure(8, weight=2)  
        vLig = 0
        Label (self.nbTab3, text = "Moyens Mat�riels Engag�s", fg = "blue", bg = "darkgray").grid(row = vLig, column = 0, columnspan = 9, sticky = W+E)
        vLig += 1

        Label (self.nbTab3, text = "H�licopt�res S�curit� Civile : ").grid(row = vLig, column = 0, sticky = W)
        self.eHeliSC = Entry (self.nbTab3)
        self.eHeliSC.grid (row = vLig, column = 1, sticky = W)
        Label (self.nbTab3, text = "H�licopt�res Militaires : ").grid(row = vLig, column = 3, sticky = W)
        self.eHeliMil = Entry (self.nbTab3)
        self.eHeliMil.grid (row = vLig, column = 4, sticky = W)
        Label (self.nbTab3, text = "Groupes �lectrog�nes : ").grid(row = vLig, column = 6, sticky = W)
        self.eGrpElec = Entry (self.nbTab3)
        self.eGrpElec.grid (row = vLig, column = 7, sticky = W+E)
        vLig += 1

        Label (self.nbTab3, text = "Autres : ").grid(row = vLig, column = 0, sticky = W)
        self.eAutres = Entry (self.nbTab3)
        self.eAutres.grid (row = vLig, column = 1, columnspan = 3, sticky = W+E)
        vLig += 1

        self.notebook.setnaturalsize()
        vLigne += 4
        Label (vFen,text="Final du message ", fg="blue",bg="cyan").grid(row=vLigne, column = 0, columnspan = 8, sticky = W+E)
        vLigne += 1
        Label (vFen, text="GDH D�p�t/R�daction : ").grid(row=vLigne, column=0, sticky=W)
        self.efGdhDep = Commun.gdhWidget(vFen, vFen)
        self.efGdhDep.grid (row=vLigne, column=1, sticky=W)
        self.rbACK = Pmw.RadioSelect(vFen, buttontype="radiobutton",labelpos=W,label_text="Demande Accus� de R�ception : ")
        self.rbACK.grid(row=vLigne, column=4, columnspan=3, sticky=W)
        self.rbACK.add("Oui")
        self.rbACK.add("Non")
        vLigne += 1
      
        Label (vFen,text = "Fin de Message ", fg = "blue",bg = "orange").grid(row = vLigne, column = 0, columnspan = 8, sticky = W+E)
        vLigne += 1

        Button (vFen, text = "Valider", command = self.validerBT, fg = "red", underline = 0).grid(row = vLigne, column = 1, padx = 5, pady = 5, sticky = W+E)
        Button (vFen, text = "Annuler", command = self.annulerBT, fg = "red", underline = 1).grid(row = vLigne, column = 4, padx = 5, pady = 5, sticky = W+E)
        Button (vFen, text = "Quitter", command = self.quitterBT, fg = "red", underline = 0).grid(row = vLigne, column = 7, padx = 5, pady = 5, sticky = W+E)
        

    # Action sur un bouton "Valider"
    def validerBT(self, evt = None):
        "Traitement du bouton 'Valider'"

        #Contr�le de la validit� des donn�es
        if self.controleSaisie() == False:
            # Si erreur, on stoppe le traitement
            return None

        # Recalcul des donn�es variables (Gdh, N� message, etc...)
        if self.iGdh.get() == True :
            self.efGdh.setvalue("")
            vGdh = datetime.datetime.now().strftime("%d/%m/%y %H:%M")
            self.efGdh.setvalue(vGdh)
            
        # R�daction du message
        self.redigerBT()

        # Impression
        if self.root.userData['IMPR_MSG'] == "OUI" :
            os.startfile(Commun.getFullPath(self.root, self.vFicBT+".TXT"), "print")
        else :
            tkMessageBox.showinfo('Message BT', 'Message cr�� : ' + self.vFicBT)
            
        self.fenetre.destroy()


        
    # Action sur le bouton "Annuler"
    def annulerBT(self, evt = None):
        "Traitement du bouton 'Annuler'"
        # Remise � Z�ro de la saisie
        self.razSaisie()


    # Action sur le bouton "Annuler"
    def quitterBT(self, evt = None):
        "Traitement du bouton 'Quitter'"
        etesVousSur = tkMessageBox.askquestion("Fermeture du Formulaire", \
                                               "Confirmez-vous la fermeture du Bilan Temporaire ?")
        if etesVousSur == "yes" :
            self.fenetre.destroy()
        else:
            self.fenetre.focus_set()


    def controleSaisie(self):
        if not (self.efGdh.valid() and self.cbEmetteur.valid() and self.cbDestinataire.valid() and \
                self.efOrigine.valid() and self.efDestAction.valid()):
            tkMessageBox.showwarning('Contr�le', 'Les champs en rouge sont absents ou incorrects')
            self.fenetre.focus_set()
            return False
        
        return True


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
        self.cbDegUrg.selectitem(self.root.userData['URG_BT'])
        vTime = datetime.datetime.now().strftime("%H:%M")
        self.efObjet.setvalue(u"Bilan temporaire � " + vTime)
        self.eDptAET.delete(0,END)
        self.eDptTNA.delete(0,END)
        self.eDptANT.delete(0,END)
        self.cbORSEC.setentry("")
        self.cbPortee.setentry("")
        self.rbCrise.invoke("Non")
        self.eDecedes.delete(0,END)
        self.eBlesses.delete(0,END)
        self.eDeplaces.delete(0,END)
        self.eInterv.delete(0,END)
        self.eHeli.delete(0,END)
        self.eAxes.delete(0,END)
        self.eSansEau.delete(0,END)
        self.eSansElec.delete(0,END)
        self.eSansTel.delete(0,END)
        self.eSPLoc.delete(0,END)
        self.eSPExt.delete(0,END)
        self.eMilSC.delete(0,END)
        self.ePolice.delete(0,END)
        self.eArmee.delete(0,END)
        self.eAssoSC.delete(0,END)
        self.eElec.delete(0,END)
        self.eTelecom.delete(0,END)
        self.eEquip.delete(0,END)
        self.eHeliSC.delete(0,END)
        self.eHeliMil.delete(0,END)
        self.eGrpElec.delete(0,END)
        self.eAutres.delete(0,END)
        self.efGdhDep.setvalue(vGdh)
        self.rbACK.invoke("Non")
        

    # Creation des fichiers message BT
    def redigerBT(self):

        # Nom du fichier
        self.vFicBT = Commun.getFicBT(self.root)
        # Fichier TXT
        self.txtFileBT()
        # Fichier XML
        self.xmlFileBT()
        
        # Ecriture d'une ligne dans la main courante
        vTexte = "Message " + self.vFicBT + \
		         " de " + self.efOrigine.getvalue() + " vers " +  self.efDestAction.getvalue()
        infosMCI = Commun.InfosMCI(self.efGdh.getvalue(), self.cbEmetteur.get(), self.cbDestinataire.get(), \
                                   self.cbDegUrg.get(), " ", vTexte)
        infosMCI.ecrire(self.root)
 

    def txtFileBT(self):
    
        fic = open(Commun.getFullPath(self.root, self.vFicBT+".TXT"),'w')

        fic.write(self.vFicBT+"\n\n")
        fic.write('################################################################################\n')
        fic.write('- ' +(self.root.userData['ACTIVATION'] + ' - ')*3+'\n')
        fic.write('--------------------------------------------------------------------------------\n')

        # Informations transmission
        fic.write("GDH Emission : " + Commun.encode(self.efGdh.getvalue())+ "\n")
        fic.write("Emis par     : " + Commun.encode(self.cbEmetteur.get())+ "\n")
        fic.write("Re�u par     : " + Commun.encode(self.cbDestinataire.get())+ "\n")
        fic.write("Instructions : " + Commun.encode(self.eInstruc.get())+ "\n")
        fic.write('================================================================================\n')

        # Ent�te du message
        fic.write("MESSAGE BILAN TEMPORAIRE".center(80) + "\n")
        fic.write("Origine      : " + Commun.encode(self.efOrigine.get())+ "\n")
        fic.write("Dest. Action : " + Commun.encode(self.efDestAction.get())+ "\n")
        fic.write("Dest. Info   : " + Commun.encode(self.eDestInfo.get())+ "\n")
        fic.write("Urgence      : " + Commun.encode(self.cbDegUrg.get())+ "\n")
        fic.write("--------------------------------------------------------------------------------\n")

        # Corps du message
        fic.write("Objet        : " + Commun.encode(self.efObjet.getvalue())+ "\n")
        fic.write("Niveau d'alerte\n")
        fic.write("D�pt. Alert� et Touch� : " + Commun.encode(self.eDptAET.get())+ "\n")
        fic.write("Touch� et Non Alert�   : " + Commun.encode(self.eDptTNA.get())+ "\n")
        fic.write("Alert� et Non Touch�   : " + Commun.encode(self.eDptANT.get())+ "\n")
        fic.write("Plan ORSEC             : " + Commun.encode(self.cbORSEC.get())+ "\n")
        fic.write("Port�e ORSEC           : " + Commun.encode(self.cbPortee.get())+ "\n")
        fic.write("Cell. de Crise activ�e : " + Commun.encode(self.rbCrise.getvalue())+ "\n")
        fic.write("--------------------------------------------------------------------------------\n")
        fic.write("Bilans Humain et Mat�riel\n")
        fic.write("Nb D�c�d�s       : " + Commun.encode(self.eDecedes.get())+ "\n")
        fic.write("Nb Bless�s       : " + Commun.encode(self.eBlesses.get())+ "\n")
        fic.write("Nb D�plac�s      : " + Commun.encode(self.eDeplaces.get())+ "\n")
        fic.write("Nb Interventions : " + Commun.encode(self.eInterv.get())+ "\n")
        fic.write("Nb H�litreuill�s : " + Commun.encode(self.eHeli.get())+ "\n")
        fic.write("Nb Axes coup�s   : " + Commun.encode(self.eAxes.get())+ "\n")
        fic.write("Foyers priv�s d'Eau       : " + Commun.encode(self.eSansEau.get())+ "\n")
        fic.write("Foyers priv�s Electricit� : " + Commun.encode(self.eSansElec.get())+ "\n")
        fic.write("Foyers priv�s Telephone   : " + Commun.encode(self.eSansTel.get())+ "\n")
        fic.write("--------------------------------------------------------------------------------\n")
        fic.write("Effectifs engag�s\n")
        fic.write("SP Locaux             : " + Commun.encode(self.eSPLoc.get())+ "\n")
        fic.write("SP Extra zonaux       : " + Commun.encode(self.eSPExt.get())+ "\n")
        fic.write("Mil. S�curit� Civile  : " + Commun.encode(self.eMilSC.get())+ "\n")
        fic.write("Police/Gendarmerie    : " + Commun.encode(self.ePolice.get())+ "\n")
        fic.write("Militaires            : " + Commun.encode(self.eArmee.get())+ "\n")
        fic.write("Asso. S�curit� Civile : " + Commun.encode(self.eAssoSC.get())+ "\n")
        fic.write("EDF / GDF             : " + Commun.encode(self.eElec.get())+ "\n")
        fic.write("France T�lecom        : " + Commun.encode(self.eTelecom.get())+ "\n")
        fic.write("DDE/DIR/CG            : " + Commun.encode(self.eEquip.get())+ "\n")
        fic.write("--------------------------------------------------------------------------------\n")
        fic.write("Moyens Mat�riels Engag�s\n")
        fic.write("H�licopt�res S�curit� Civile : " + Commun.encode(self.eHeliSC.get())+ "\n")
        fic.write("H�licopt�res Militaires      : " + Commun.encode(self.eHeliMil.get())+ "\n")
        fic.write("Groupes �lectrog�nes         : " + Commun.encode(self.eGrpElec.get())+ "\n")
        fic.write("Autres                       : " + Commun.encode(self.eAutres.get())+ "\n")
        fic.write('--------------------------------------------------------------------------------\n')

        # Final du message
        fic.write("GDH D�p�t    : " + Commun.encode (self.efGdhDep.getvalue())+"\n")
        fic.write("Demande A.R. : " + Commun.encode (self.rbACK.getvalue())+"\n")
        fic.write("FIN DE MESSAGE".center(80) + "\n")
        fic.write('================================================================================\n')
        fic.write('- ' +(self.root.userData['ACTIVATION'] + ' - ')*3+'\n')
        fic.write('################################################################################\n')

        fic.close()

    #
    def xmlFileBT(self):

        fic = open(Commun.getFullPath(self.root, self.vFicBT+".XML"),'w')
        
        fic.write('<?xml version="1.0" encoding="iso-8859-15"?><?xml-stylesheet type="text/xsl" href="..\msgBT.XSL"?>\n')
        fic.write('<msg>\n')
        fic.write('<form>Message OBNT</form>\n')
        fic.write('<soft>' + self.root.userData['LOGICIEL'] + '</soft>\n')
        fic.write('<vers>' + self.root.userData['VERSION'] + '</vers>\n')
        fic.write('<mode>' + self.root.userData['ACTIVATION'] + '</mode>\n')
        fic.write('<trans>\n')
        fic.write('<gdh>' + Commun.encode(self.efGdh.getvalue())+'</gdh>\n')
        fic.write('<emis>' + Commun.encode(self.cbEmetteur.get())+'</emis>\n')
        fic.write('<recu>' + Commun.encode(self.cbDestinataire.get())+"</recu>\n")
        fic.write("<instr>" + Commun.encode(self.eInstruc.get())+"</instr>\n")
        fic.write('</trans>\n')
        fic.write("<top>\n")
        fic.write("<from>" + Commun.encode(self.efOrigine.getvalue())+"</from>\n")
        fic.write("<to>" + Commun.encode(self.efDestAction.getvalue())+"</to>\n")
        fic.write("<info>" + Commun.encode(self.eDestInfo.get())+"</info>\n")
        fic.write("<urg>" + Commun.encode(self.cbDegUrg.get())+"</urg>\n")
        fic.write('</top>\n')
        fic.write("<corps>\n")
        fic.write("<obj>" + Commun.encode(self.efObjet.getvalue())+"</obj>\n")
        fic.write("<dptaet>" + Commun.encode(self.eDptAET.get())+ "</dptaet>\n")
        fic.write("<dpttna>" + Commun.encode(self.eDptTNA.get())+ "</dpttna>\n")
        fic.write("<dptant>" + Commun.encode(self.eDptANT.get())+ "</dptant>\n")
        fic.write("<orsec>" + Commun.encode(self.cbORSEC.get())+ "</orsec>\n")
        fic.write("<portee>" + Commun.encode(self.cbPortee.get())+ "</portee>\n")
        fic.write("<crise>" + Commun.encode(self.rbCrise.getvalue())+ "</crise>\n")
        fic.write("<ong1>\n")
        fic.write("<dcd>" + Commun.encode(self.eDecedes.get())+ "</dcd>\n")
        fic.write("<blesse>" + Commun.encode(self.eBlesses.get())+ "</blesse>\n")
        fic.write("<deplace>" + Commun.encode(self.eDeplaces.get())+ "</deplace>\n")
        fic.write("<interv>" + Commun.encode(self.eInterv.get())+ "</interv>\n")
        fic.write("<heli>" + Commun.encode(self.eHeli.get())+ "</heli>\n")
        fic.write("<axe>" + Commun.encode(self.eAxes.get())+ "</axe>\n")
        fic.write("<sanseau>" + Commun.encode(self.eSansEau.get())+ "</sanseau>\n")
        fic.write("<sanselec>" + Commun.encode(self.eSansElec.get())+ "</sanselec>\n")
        fic.write("<sanstel>" + Commun.encode(self.eSansTel.get())+ "</sanstel>\n")
        fic.write("</ong1>\n")
        fic.write("<ong2>\n")
        fic.write("<sploc>" + Commun.encode(self.eSPLoc.get())+ "</sploc>\n")
        fic.write("<spext>" + Commun.encode(self.eSPExt.get())+ "</spext>\n")
        fic.write("<milsc>" + Commun.encode(self.eMilSC.get())+ "</milsc>\n")
        fic.write("<police>" + Commun.encode(self.ePolice.get())+ "</police>\n")
        fic.write("<armee>" + Commun.encode(self.eArmee.get())+ "</armee>\n")
        fic.write("<assosc>" + Commun.encode(self.eAssoSC.get())+ "</assosc>\n")
        fic.write("<elec>" + Commun.encode(self.eElec.get())+ "</elec>\n")
        fic.write("<telecom>" + Commun.encode(self.eTelecom.get())+ "</telecom>\n")
        fic.write("<equip>" + Commun.encode(self.eEquip.get())+ "</equip>\n")
        fic.write("</ong2>\n")
        fic.write("<ong3>\n")
        fic.write("<helisc>" + Commun.encode(self.eHeliSC.get())+ "</helisc>\n")
        fic.write("<helimil>" + Commun.encode(self.eHeliMil.get())+ "</helimil>\n")
        fic.write("<grpelec>" + Commun.encode(self.eGrpElec.get())+ "</grpelec>\n")
        fic.write("<autre>" + Commun.encode(self.eAutres.get())+ "</autre>\n")
        fic.write("</ong3>\n")
        fic.write('</corps>\n')
        fic.write('<bot>\n')
        fic.write("<gdh>" + Commun.encode(self.efGdhDep.getvalue())+"</gdh>\n")
        fic.write("<ack>" + Commun.encode(self.rbACK.getvalue())+"</ack>\n")
        fic.write('</bot>\n')
            
        fic.write('</msg>\n')
    
        fic.close()
    #
