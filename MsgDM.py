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


###################### Creation d'un message DM.
class FormDM:
    "Classe définissant le formulaire Demande de Moyens"
    
    def __init__(self, appli):
        "Constructeur de la fenêtre DM"

        self.root = appli # Référence à l'application racine

        # Création de la nouvelle fenêtre
        self.fenetre = Commun.nouvelleFenetre(self.root, "Message de Demande de Moyens")
        # Fermeture par la case système
        self.fenetre.protocol("WM_DELETE_WINDOW", self.quitterDM)

        # Composants de la fenêtre
        self.dessineDM()

        # Initialisations
        self.razSaisie()        
        
        # Gestion des raccourcis clavier
        self.fenetre.bind('<Alt-v>', self.validerDM)
        self.fenetre.bind('<Return>', self.validerDM)
        self.fenetre.bind('<Alt-n>', self.annulerDM)
        self.fenetre.bind('<Escape>', self.annulerDM)
        self.fenetre.bind('<Alt-q>', self.quitterDM)

        
    def dessineDM(self):

        # variables locales
        vLigne = 1 # N° de ligne pour le positionnement des composants
        vNomBouton = ""
        vIndice = 0
        vFen = self.fenetre

        # Composants de la fenêtre
        Label (vFen,text = "Informations transmission", fg = "blue",bg = "orange").grid(row = vLigne, column = 0, columnspan = 8, sticky = W+E)
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
        self.cbDestinataire.grid (row = vLigne, column = 4, sticky = W)
        vLigne += 1
        Label (vFen, text = "Instructions particulières : ").grid(row = vLigne, column = 0, sticky = W)
        self.eInstruc = Entry (vFen)
        self.eInstruc.grid (row = vLigne, column = 1, columnspan = 4, sticky = W+E)
        vLigne += 1

        Label (vFen, text = "Message Demande de Moyens", fg = "blue",bg = "orange").grid(row = vLigne, column = 0, columnspan = 8, sticky = W+E)
        vLigne += 1

        Label (vFen, text = "Entête du message", fg = "blue",bg = "cyan").grid(row = vLigne, column = 0, columnspan = 8, sticky = W+E)
        vLigne += 1
        Label (vFen, text = "Origine : ").grid(row = vLigne, column = 0, sticky = W)
        self.efOrigine = Pmw.EntryField (vFen, validate = Commun.nonVideValidator)
        self.efOrigine.grid (row = vLigne, column = 1, sticky = W)
        vLigne = vLigne +1
        Label (vFen, text = "Destinataires Action : ").grid(row = vLigne, column = 0, sticky = W)
        self.efDestAction = Pmw.EntryField (vFen, validate = Commun.nonVideValidator)
        self.efDestAction.grid (row = vLigne, column = 1, columnspan = 4, sticky = E+W)
        Label (vFen, text = "(utilisez le / comme séparateur)").grid(row = vLigne, rowspan = 2, column = 5, columnspan = 2, sticky = W)
        vLigne += 1
        Label (vFen, text = "Destinataires Info : ").grid(row = vLigne, column = 0, sticky = W)
        self.eDestInfo = Entry (vFen)
        self.eDestInfo.grid (row = vLigne, column = 1, columnspan = 4, sticky = E+W)
        vLigne += 1
        Label (vFen, text = "Degré d'Urgence : ").grid(row = vLigne, column = 0, sticky = W)
        self.cbDegUrg = Commun.comboWidget (self.root, vFen, self.root.cfgListe['DegUrgOBNT'])
        self.cbDegUrg.grid (row = vLigne, column = 1, columnspan = 2, sticky = W)
        vLigne += 1

        Label (vFen, text = "Corps du message ", fg = "blue",bg = "cyan").grid(row = vLigne, column = 0,columnspan = 8, sticky = E+W)
        vLigne += 1
        Label (vFen, text = "Objet : ").grid(row = vLigne, column = 0, sticky = W)
        self.efObjet = Pmw.EntryField (vFen, validate = Commun.nonVideValidator)
        self.efObjet.grid (row = vLigne, column = 1, columnspan = 6, sticky = W+E)
        vLigne += 1
        Label (vFen, text = "Zone de défense : ").grid(row = vLigne, column = 0, sticky = W)
        self.cbZoneDef = Commun.comboWidget (self.root, vFen, self.root.cfgListe['ZoneDef'])
        self.cbZoneDef.grid (row = vLigne, column = 1,  columnspan = 2, sticky = W)
        Label (vFen, text = "Département : ").grid(row = vLigne, column = 3, sticky = W)
        self.eDept = Entry (vFen)
        self.eDept.grid (row = vLigne, column = 4, sticky = W)
        vLigne += 1

        self.notebook = Pmw.NoteBook(vFen)
        self.notebook.grid(row = vLigne, column = 0, columnspan = 8, sticky = W+E)
        self.nbTab1 = self.notebook.add('Personnels')
        self.nbTab1.grid_columnconfigure(1, weight=2)  
        self.nbTab1.grid_columnconfigure(4, weight=2)  
        self.nbTab1.grid_columnconfigure(7, weight=2)  
        self.nbTab1.grid_columnconfigure(8, weight=2)  
        vLig = 0
        Label (self.nbTab1,text = "Demande de personnel(s) ", fg = "blue",bg = "darkgray").grid(row = vLig, column = 0,columnspan = 9, sticky = W+E)    
        vLig += 1

        Label (self.nbTab1, text = "Sécurité Civile : ").grid(row = vLig, column = 0, sticky = W)
        self.ePersSC = Entry (self.nbTab1)
        self.ePersSC.grid (row = vLig, column = 1 , sticky = W)
        Label (self.nbTab1, text = "Militaires : ").grid(row = vLig, column = 3, sticky = W)
        self.ePersMil = Entry (self.nbTab1)
        self.ePersMil.grid (row = vLig, column = 4 , sticky = W)
        Label (self.nbTab1, text = "Autre : ").grid(row = vLig, column = 6, sticky = W)
        self.ePersAutre = Entry (self.nbTab1)
        self.ePersAutre.grid (row = vLig, column = 7 , sticky = W)
        vLig += 1

        self.nbTab2 = self.notebook.add('Moyens')
        self.nbTab2.grid_columnconfigure(1, weight=2)  
        self.nbTab2.grid_columnconfigure(4, weight=2)  
        self.nbTab2.grid_columnconfigure(7, weight=2)  
        self.nbTab2.grid_columnconfigure(8, weight=2)
        vLig = 0
        Label (self.nbTab2,text = "Moyen(s) Aérien(s)", fg = "blue",bg = "darkgray").grid(row = vLig, column = 0,columnspan = 9, sticky = W+E) 
        vLig += 1
        
        Label (self.nbTab2, text = "Hélicoptère : ").grid(row = vLig, column = 0, sticky = W)
        self.eHelico = Entry (self.nbTab2)
        self.eHelico.grid (row = vLig, column = 1 , sticky = W)
        Label (self.nbTab2, text = "Avion : ").grid(row = vLig, column = 3, sticky = W)
        self.eAvion = Entry (self.nbTab2)
        self.eAvion.grid (row = vLig, column = 4 , sticky = W)
        vLig += 1

        Label (self.nbTab2,text = "Moyen(s) Terrestres(s)", fg = "blue",bg = "darkgray").grid(row = vLig, column = 0,columnspan = 9, sticky = W+E) 
        vLig += 1

        Label (self.nbTab2, text = "Engin(s) TP : ").grid(row = vLig, column = 0, sticky = W)
        self.eEnginTP = Entry (self.nbTab2)
        self.eEnginTP.grid (row = vLig, column = 1 , sticky = W)
        Label (self.nbTab2, text = "Grue(s) : ").grid(row = vLig, column = 3, sticky = W)
        self.eGrue = Entry (self.nbTab2)
        self.eGrue.grid (row = vLig, column = 4 , sticky = W)
        vLig += 1

        Label (self.nbTab2, text = "Autre(s)-1 : ").grid(row = vLig, column = 0, sticky = W)
        self.eAutre1 = Entry (self.nbTab2)
        self.eAutre1.grid (row = vLig, column = 1 , sticky = W)
        Label (self.nbTab2, text = "Autre(s)-2 : ").grid(row = vLig, column = 3, sticky = W)
        self.eAutre2 = Entry (self.nbTab2)
        self.eAutre2.grid (row = vLig, column = 4 , sticky = W)
        vLig += 1
        
        self.nbTab3 = self.notebook.add('Matériels')
        self.nbTab3.grid_columnconfigure(1, weight=2)  
        self.nbTab3.grid_columnconfigure(4, weight=2)  
        self.nbTab3.grid_columnconfigure(7, weight=2)  
        self.nbTab3.grid_columnconfigure(8, weight=2)  
        vLig = 0
        Label (self.nbTab3,text = "Groupe(s) électrogène(s)", fg = "blue",bg = "darkgray").grid(row = vLig, column = 0,columnspan = 9, sticky = W+E) 
        vLig += 1

        Label (self.nbTab3, text = "> 20 KVa : ").grid(row = vLig, column = 0, sticky = W)
        self.eSup20 = Entry (self.nbTab3)
        self.eSup20.grid (row = vLig, column = 1 , sticky = W)
        Label (self.nbTab3, text = "> 100 KVa : ").grid(row = vLig, column = 3, sticky = W)
        self.eSup100 = Entry (self.nbTab3)
        self.eSup100.grid (row = vLig, column = 4 , sticky = W)
        Label (self.nbTab3, text = "< 100 KVa : ").grid(row = vLig, column = 6, sticky = W)
        self.eInf100 = Entry (self.nbTab3)
        self.eInf100.grid (row = vLig, column = 7 , sticky = W)
        vLig += 1

        Label (self.nbTab3,text = "Moto(s) pompe(s)", fg = "blue",bg = "darkgray").grid(row = vLig, column = 0,columnspan = 9, sticky = W+E) 
        vLig += 1
        Label (self.nbTab3, text = "> 160 M3/H : ").grid(row = vLig, column = 0, sticky = W)
        self.eSup160 = Entry (self.nbTab3)
        self.eSup160.grid (row = vLig, column = 1 , sticky = W)
        Label (self.nbTab3, text = " = 160 M3/H : ").grid(row = vLig, column = 3, sticky = W)
        self.eEgal160 = Entry (self.nbTab3)
        self.eEgal160.grid (row = vLig, column = 4 , sticky = W)
        Label (self.nbTab3, text = "< 160 M3/H : ").grid(row = vLig, column = 6, sticky = W)
        self.eInf160 = Entry (self.nbTab3)
        self.eInf160.grid (row = vLig, column = 7 , sticky = W)
        vLig += 1

        Label (self.nbTab3,text = "Station traitement de l'eau", fg = "blue",bg = "darkgray").grid(row = vLig, column = 0,columnspan = 9, sticky = W+E) 
        vLig += 1
        Label (self.nbTab3, text = "Station Eaux Usées : ").grid(row = vLig, column = 0, sticky = W)
        self.eStaEU = Entry (self.nbTab3)
        self.eStaEU.grid (row = vLig, column = 1 , sticky = W)
        Label (self.nbTab3, text = "Station Eau Potable : ").grid(row = vLig, column = 3, sticky = W)
        self.eStaEP = Entry (self.nbTab3)
        self.eStaEP.grid (row = vLig, column = 4 , sticky = W)
        vLig += 1

        self.nbTab4 = self.notebook.add('Divers')
        self.nbTab4.grid_columnconfigure(1, weight=2)  
        self.nbTab4.grid_columnconfigure(4, weight=2)  
        self.nbTab4.grid_columnconfigure(7, weight=2)  
        self.nbTab4.grid_columnconfigure(8, weight=2)  
        vLig = 0
        Label (self.nbTab4,text = "Demande de matériel(s) Divers", fg = "blue",bg = "darkgray").grid(row = vLig, column = 0,columnspan = 9, sticky = W+E)
        vLig += 1
        Label (self.nbTab4, text = "Scie(s) : ").grid(row = vLig, column = 0, sticky = W)
        self.eScie = Entry (self.nbTab4)
        self.eScie.grid (row = vLig, column = 1 , sticky = W)
        Label (self.nbTab4, text = "Pelle(s) : ").grid(row = vLig, column = 3, sticky = W)
        self.ePelle = Entry (self.nbTab4)
        self.ePelle.grid (row = vLig, column = 4 , sticky = W)
        vLig += 1

        Label (self.nbTab4, text = "CMIR - CMIC : ").grid(row = vLig, column = 0, sticky = W)
        self.eCMIR = Entry (self.nbTab4)
        self.eCMIR.grid (row = vLig, column = 1 , sticky = W)
        Label (self.nbTab4, text = "PMA : ").grid(row = vLig, column = 3, sticky = W)
        self.ePMA = Entry (self.nbTab4)
        self.ePMA.grid (row = vLig, column = 4 , sticky = W)
        vLig += 1

        Label (self.nbTab4, text = "Autre(s)-1 : ").grid(row = vLig, column = 0, sticky = W)
        self.eMatAutre1 = Entry (self.nbTab4)
        self.eMatAutre1.grid (row = vLig, column = 1 , sticky = W)
        Label (self.nbTab4, text = "Autre(s)-2 : ").grid(row = vLig, column = 3, sticky = W)
        self.eMatAutre2 = Entry (self.nbTab4)
        self.eMatAutre2.grid (row = vLig, column = 4, sticky = W)
        vLig += 1

        self.notebook.setnaturalsize()
        vLigne += 6
        Label (vFen,text="Final du message ", fg="blue",bg="cyan").grid(row=vLigne, column=0, columnspan=8, sticky=E+W)
        vLigne += 1
        Label (vFen, text="GDH Dépôt/Rédaction : ").grid(row=vLigne, column=0, sticky=W)
        self.efGdhDep = Commun.gdhWidget(vFen, vFen)
        self.efGdhDep.grid (row=vLigne, column=1, sticky=W)
        self.rbACK = Pmw.RadioSelect(vFen, buttontype="radiobutton",labelpos=W,label_text="Demande Accusé de Réception : ")
        self.rbACK.grid(row=vLigne, column=3, columnspan=2, sticky=W)
        self.rbACK.add("Oui")
        self.rbACK.add("Non")
        vLigne += 1
      
        Label (vFen,text = "Fin de Message", fg = "blue",bg = "orange").grid(row = vLigne, column = 0, columnspan = 8, sticky = E+W)
        vLigne += 1

        Button (vFen, text = "Valider", command = self.validerDM, fg = "red", underline = 0).grid(row = vLigne, column = 1, padx = 5, pady = 5, sticky = E+W)
        Button (vFen, text = "Annuler", command = self.annulerDM, fg = "red", underline = 1).grid(row = vLigne, column = 4, padx = 5, pady = 5, sticky = E+W)
        Button (vFen, text = "Quitter", command = self.quitterDM, fg = "red", underline = 0).grid(row = vLigne, column = 7, padx = 5, pady = 5, sticky = E+W)


    # Action sur un bouton "Valider"
    def validerDM(self, evt = None):
        "Traitement du bouton 'Valider'"

        #Contrôle de la validité des données
        if self.controleSaisie() == False:
            # Si erreur, on stoppe le traitement
            return None

        # Recalcul des données variables (Gdh, N° message, etc...)
        if self.iGdh == True :
            self.efGdh.setvalue("")
            vGdh = datetime.datetime.now().strftime("%d/%m/%y %H:%M")
            self.efGdh.setvalue(vGdh)
            
        # Rédaction du message
        self.redigerDM()

        # Impression
        if self.root.userData['IMPR_MSG'] == "OUI" :
            os.startfile(Commun.getFullPath(self.root, self.vFicDM+".TXT"), "print")
        else :
            tkMessageBox.showinfo('Message DM', 'Message créé : ' + self.vFicDM)
            
        self.fenetre.destroy()

        
    # Action sur le bouton "Annuler"
    def annulerDM(self, evt = None):
        "Traitement du bouton 'Annuler'"
        # Remise à Zéro de la saisie
        self.razSaisie()


    # Action sur le bouton "Quitter"
    def quitterDM(self, evt = None):
        "Traitement du bouton 'Quitter'"
        etesVousSur = tkMessageBox.askquestion("Fermeture du Formulaire", \
                                               "Confirmez-vous la fermeture du Message DM ?")
        if etesVousSur == "yes" :
            self.fenetre.destroy()
        else:
            self.fenetre.focus_set()
            

    # Remise à zéro de la saisie utilisateur
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
        self.cbDegUrg.selectitem(self.root.userData['URG_DM'])
        vTime = datetime.datetime.now().strftime("%H:%M")
        self.efObjet.setvalue(u"Demande de Moyens à " + vTime)
        self.cbZoneDef.setentry("")
        self.eDept.delete(0,END)
        self.ePersSC.delete(0,END)
        self.ePersMil.delete(0,END)
        self.ePersAutre.delete(0,END)
        self.eHelico.delete(0,END)
        self.eAvion.delete(0,END)
        self.eEnginTP.delete(0,END)
        self.eGrue.delete(0,END)
        self.eAutre1.delete(0,END)
        self.eAutre2.delete(0,END)
        self.eSup20.delete(0,END)
        self.eSup100.delete(0,END)
        self.eInf100.delete(0,END)
        self.eSup160.delete(0,END)
        self.eEgal160.delete(0,END)
        self.eInf160.delete(0,END)
        self.eStaEU.delete(0,END)
        self.eStaEP.delete(0,END)
        self.eScie.delete(0,END)
        self.ePelle.delete(0,END)
        self.eCMIR.delete(0,END)
        self.ePMA.delete(0,END)
        self.eMatAutre1.delete(0,END)
        self.eMatAutre2.delete(0,END)
        self.efGdhDep.setvalue(vGdh) # Gdh rédaction message
        self.rbACK.invoke("Non") # Demande Ack


    # Validation de la saisie utilisateur
    def controleSaisie(self):
        if not (self.efGdh.valid() and self.cbEmetteur.valid() and self.cbDestinataire.valid() and \
                self.efOrigine.valid() and self.efDestAction.valid()):
            tkMessageBox.showwarning('Contrôle', 'Les champs en rouge sont absents ou incorrects')
            self.fenetre.focus_set()
            return False

        return True
        

    # Creation des fichiers message DM 
    def redigerDM(self):

        # Nom du fichier
        self.vFicDM = Commun.getFicDM(self.root)
        # Fichier TXT
        self.txtFileDM()
        # Fichier XML
        self.xmlFileDM()
        
        # Ecriture d'une ligne dans la main courante
        vTexte = "Message " + self.vFicDM + \
		         " de " + self.efOrigine.getvalue() + " vers " +  self.efDestAction.getvalue()
        infosMCI = Commun.InfosMCI(self.efGdh.getvalue(), self.cbEmetteur.get(), self.cbDestinataire.get(), \
                                   self.cbDegUrg.get(), " ", vTexte)
        infosMCI.ecrire(self.root)


    def txtFileDM(self):
                
        fic = open(Commun.getFullPath(self.root, self.vFicDM+".TXT"),'w')
        
        fic.write(self.vFicDM+"\n\n")
        fic.write('################################################################################\n')
        fic.write('- ' +(self.root.userData['ACTIVATION'] + ' - ')*3+'\n')
        fic.write('--------------------------------------------------------------------------------\n')

        # Informations transmission
        fic.write("GDH Emission : " + self.efGdh.getvalue()+ "\n")
        fic.write("Emis par     : " + self.cbEmetteur.get()+ "\n")
        fic.write("Reçu par     : " + self.cbDestinataire.get()+ "\n")
        fic.write("Instructions : " + self.eInstruc.get()+ "\n")
        fic.write("================================================================================\n")

        # Entête du message
        fic.write("MESSAGE DEMANDE DE MOYENS".center(80) + "\n")
        fic.write("Origine      : " + self.efOrigine.get()+ "\n")
        fic.write("Dest. Action : " + self.efDestAction.get()+ "\n")
        fic.write("Dest. Info   : " + self.eDestInfo.get()+ "\n")
        fic.write("Urgence      : " + self.cbDegUrg.get()+"\n")
        fic.write("--------------------------------------------------------------------------------\n")

        # Corps du message
        fic.write("Objet        : " + self.efObjet.getvalue()+"\n")
        fic.write("Zone Défense : " + self.cbZoneDef.get()+"\n")
        fic.write("Département  : " + self.eDept.get()+"\n")
        fic.write("--------------------------------------------------------------------------------\n")

        # Demande de personnel(s) 
        fic.write("Demande de Personnels\n")
        fic.write("Séc. Civile  : " + self.ePersSC.get()+"\n")
        fic.write("Militaires   : " + self.ePersMil.get()+"\n")
        fic.write("Autre        : " + self.ePersAutre.get()+"\n")
        fic.write("--------------------------------------------------------------------------------\n")

        # Demande de moyen(s)
        fic.write("Moyen(s) Aérien(s)\n")
        fic.write("Hélicoptère  : " + self.eHelico.get()+"\n")
        fic.write("Avion        : " + self.eAvion.get()+"\n")

        fic.write("Moyen(s) Terrestre(s)\n")
        fic.write("Engin(s) TP  : " + self.eEnginTP.get()+"\n")
        fic.write("Grue(s)      : " + self.eGrue.get()+"\n")

        fic.write("Autre(s)-1   : " + self.eAutre1.get()+"\n")
        fic.write("Autre(s)-2   : " + self.eAutre2.get()+"\n")
        fic.write("--------------------------------------------------------------------------------\n")
        
        # Demande de matériel(s)
        fic.write("Groupe(s) électrogène(s) \n")
        fic.write("> 20 KVa     : " + self.eSup20.get()+"\n")
        fic.write("> 100 KVa    : " + self.eSup100.get()+"\n")
        fic.write("< 100 KVa    : " + self.eInf100.get()+"\n")

        fic.write("Moto(s) pompe(s) \n")
        fic.write("> 160 M3/H   : " + self.eSup160.get()+"\n")
        fic.write("= 160 M3/H   : " + self.eEgal160.get()+"\n")
        fic.write("< 160 M3/H   : " + self.eInf160.get()+"\n")

        fic.write("Traitement de l'eau \n")
        fic.write("Station EP   : " + self.eStaEP.get()+"\n")
        fic.write("Station EU   : " + self.eStaEU.get()+"\n")
        fic.write("--------------------------------------------------------------------------------\n")

        fic.write("Demande de matériel(s) Divers\n")
        fic.write("Scie(s)      : " + self.eScie.get()+"\n")
        fic.write("Pelle(s)     : " + self.ePelle.get()+"\n")
        fic.write("CMIR - CMIC  : " + self.eCMIR.get()+"\n")
        fic.write("PMA          : " + self.ePMA.get()+"\n")
        fic.write("Autre(s)-1   : " + self.eMatAutre1.get()+"\n")
        fic.write("Autre(s)-2   : " + self.eMatAutre2.get()+"\n")
        fic.write("\n")
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
    def xmlFileDM(self):

        fic = open(Commun.getFullPath(self.root, self.vFicDM+".XML"),'w')
        
        fic.write('<?xml version="1.0" encoding="iso-8859-15"?><?xml-stylesheet type="text/xsl" href="..\msgDM.XSL"?>\n')
        fic.write('<msg>\n')
        fic.write('<form>Message DM</form>\n')
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
        fic.write("<zdef>" + self.cbZoneDef.get()+"</zdef>\n")
        fic.write("<dpt>" + self.eDept.get()+"</dpt>\n")
        fic.write("<ong1>\n")
        fic.write("<secciv>" + self.ePersSC.get()+"</secciv>\n")
        fic.write("<mili>" + self.ePersMil.get()+"</mili>\n")
        fic.write("<autre>" + self.ePersAutre.get()+"</autre>\n")
        fic.write("</ong1>\n")
        fic.write("<ong2>\n")
        fic.write("<helico>" + self.eHelico.get()+"</helico>\n")
        fic.write("<avion>" + self.eAvion.get()+"</avion>\n")
        fic.write("<engin>" + self.eEnginTP.get()+"</engin>\n")
        fic.write("<grue>" + self.eGrue.get()+"</grue>\n")
        fic.write("<aut-1>" + self.eAutre1.get()+"</aut-1>\n")
        fic.write("<aut-2>" + self.eAutre2.get()+"</aut-2>\n")
        fic.write("</ong2>\n")
        fic.write("<ong3>\n")
        fic.write("<sup20>" + self.eSup20.get()+"</sup20>\n")
        fic.write("<sup100>" + self.eSup100.get()+"</sup100>\n")
        fic.write("<inf100>" + self.eInf100.get()+"</inf100>\n")
        fic.write("<sup160>" + self.eSup160.get()+"</sup160>\n")
        fic.write("<egal160>" + self.eEgal160.get()+"</egal160>\n")
        fic.write("<inf160>" + self.eInf160.get()+"</inf160>\n")
        fic.write("<staep>" + self.eStaEP.get()+"</staep>\n")
        fic.write("<staeu>" + self.eStaEU.get()+"</staeu>\n")
        fic.write("</ong3>\n")
        fic.write("<ong4>\n")
        fic.write("<scie>" + self.eScie.get()+"</scie>\n")
        fic.write("<pelle>" + self.ePelle.get()+"</pelle>\n")
        fic.write("<cmic>" + self.eCMIR.get()+"</cmic>\n")
        fic.write("<pma>" + self.ePMA.get()+"</pma>\n")
        fic.write("<aut-1>" + self.eMatAutre1.get()+"</aut-1>\n")
        fic.write("<aut-2>" + self.eMatAutre2.get()+"</aut-2>\n")
        fic.write("</ong4>\n")
        fic.write('</corps>\n')
        fic.write('<bot>\n')
        fic.write("<gdh>" + self.efGdhDep.getvalue()+"</gdh>\n")
        fic.write("<ack>" + self.rbACK.getvalue()+"</ack>\n")
        fic.write('</bot>\n')
            
        fic.write('</msg>\n')
    
        fic.close()
    #
