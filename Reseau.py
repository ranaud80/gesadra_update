# -*- coding: iso-8859-15 -*-

from tkinter import *
from tkinter.scrolledtext import ScrolledText
 
import datetime
import time
import os
import tkinter.messagebox as tkMessageBox
import Pmw

# Modules Techniques de GesADRA
import Commun            # Fonctions Principales


class FormReseau:
    """Classe définissant la fenêtre Réseau"""
    
    def __init__(self, appli):
        """Constructeur de la fenêtre Réseau"""

        self.root = appli
        self.vFen = self.root.notebook.insert('Gestion du Réseau', before=0)
        self.num = IntVar()

        # Composants de la fenêtre
        self.drawReseau()
        
        # Initialisations
        self.selectTab()
        self.fOpeHide()

#
	
    def drawReseau(self):

        # variables locales
        vFen = self.vFen
        vLigne = 1 # N° de ligne pour le positionnement des composants

        # Frame contenant les informations de session
        Label (vFen, text = "Station locale", fg = "blue",bg = "orange").grid(row = vLigne, column = 0, columnspan = 10, sticky = E+W)
        vLigne += 1

        Label (vFen,text = "Votre station : ").grid(row = vLigne, column = 0, columnspan = 2, sticky = E)
        self.vous = StringVar()
        Label (vFen, textvariable = self.vous, font=self.root.fonteFixe).grid(row=vLigne, column=2, columnspan = 4, sticky=W)
        vLigne += 1

        Label (vFen, text = "Gestion du Réseau", fg = "blue",bg = "orange").grid(row = vLigne, column = 0, columnspan = 10, sticky = E+W)
        vLigne += 1

        # Frame des stations (uniquement pour gérer l'affichage)
        Label(vFen, text="Indicatif").grid(row=vLigne, column = 0, sticky = W)
        Label(vFen, text="Alias Tactique").grid(row=vLigne, column = 1, sticky = W)
        Label(vFen, text="Opérateur(s)").grid(row=vLigne, column = 2, sticky = W)
        Label(vFen, text="Statut").grid(row=vLigne, column = 3, sticky = W)
        Label(vFen, text="Localisation").grid(row=vLigne, column = 4, sticky = W)
        Label(vFen, text="X <-- Coordonnées --> Y").grid(row=vLigne, column = 5, columnspan = 2, sticky = W+E)
        Label(vFen, text="Commentaires").grid(row=vLigne, column = 7, columnspan = 2, sticky = W+E)
        vLigne += 1
		
        fLog = Frame(vFen)
        fLog.grid(row = vLigne, column = 0, columnspan = 10)
        sbListe = Scrollbar(fLog, orient = VERTICAL)
        self.lbListe = Listbox(fLog, height = 15, width = 140, font = self.root.fonteFixe, yscrollcommand = sbListe.set)
        self.lbListe.grid(row = vLigne, column = 0, sticky = E+W)
        self.lbListe.bind("<ButtonRelease-1>", self.select)
        self.lbListe.bind("<Double-1>", self.modifier)
        sbListe.config(command = self.lbListe.yview)
        sbListe.grid(row = vLigne, column = 1, sticky = N+S)
        vLigne += 6
        
        fBtn = Frame(vFen)
        fBtn.grid(row = vLigne, column = 0, columnspan = 10)
        self.pbUp = Button (vFen, text = "^", width = 3, command = lambda sens = "-": self.swap(sens), fg = "blue")
        self.pbUp.grid (row = vLigne, column = 0, sticky = E)
        self.pbDown = Button (vFen, text = "v", width = 3, command = lambda sens = "+":self.swap(sens), fg = "blue")
        self.pbDown.grid (row = vLigne, column = 1, sticky = W)
        self.pbUp.grid_remove()  # Caché car non opérationnel
        self.pbDown.grid_remove()# Caché car non opérationnel
        self.pbAjouter = Button (vFen, text = "Ajouter", width = 12, command = self.ajouterStation, fg = "red", underline = 4)
        self.pbAjouter.grid (row = vLigne, column = 3)
        self.pbModifier = Button (vFen, text = "Modifier", width = 12, command = self.modifier, fg = "red", underline = 1)
        self.pbModifier.grid (row = vLigne, column = 5)
        self.pbSupprimer = Button (vFen, text = "Supprimer", width = 12, command = self.supprimer, fg = "red", underline = 0)
        self.pbSupprimer.grid (row = vLigne, column = 7)
        vLigne += 1
        
        texte = Label (vFen, text = "").grid(row = vLigne, column = 0, sticky = W)
        vLigne += 1

        self.fOpe = LabelFrame(vFen, bd = 2)
        self.fOpe.grid(row = vLigne, column = 0, columnspan = 10, sticky = N+S)
        Label (self.fOpe, text = "Info Station", fg = "blue",bg = "orange").grid(row = vLigne, column = 0, columnspan = 10, sticky = E+W)
        vLigne += 1

        Label(self.fOpe, text="Indicatif").grid(row=vLigne, column = 1, sticky = W)
        Label(self.fOpe, text="Alias Tactique").grid(row=vLigne, column = 2, sticky = W)
        Label(self.fOpe, text="Opérateur(s)").grid(row=vLigne, column = 3, sticky = W)
        Label(self.fOpe, text="Statut").grid(row=vLigne, column = 4, sticky = W)
        Label(self.fOpe, text="Localisation").grid(row=vLigne, column = 5, sticky = W)
        Label(self.fOpe, text="X  <--- Coordonnées --->  Y").grid(row=vLigne, column = 6, columnspan = 2, sticky = W+E)
        Label(self.fOpe, text="Commentaires").grid(row=vLigne, column = 8, columnspan = 2, sticky = W)
        vLigne += 1

        self.efIndicatif = Pmw.EntryField(self.fOpe, validate = {"validator" : Commun.indicatifValidator, "max" : 8, "maxstrict" : False})
        self.efIndicatif.component('entry').config(width = 9)
        self.efIndicatif.component('entry').bind('<Key>', Commun.uppercaseKey)
        self.efIndicatif.grid(row = vLigne, column = 1, sticky = E+W)
        self.root.bulle.bind(self.efIndicatif, "Indicatif de 2 à 8 car., sans espace (tiret, slash et souligné permis)")
        self.efTactic = Pmw.EntryField(self.fOpe, validate = {"validator" : Commun.tacticValidator, "max" : 12, "maxstrict" : False})
        self.efTactic.component('entry').config(width = 13)
        self.efTactic.component('entry').bind('<Key>', Commun.uppercaseKey)
        self.efTactic.grid(row = vLigne, column = 2, sticky = E+W)
        self.root.bulle.bind(self.efTactic, "Alias de 2 à 12 car., sans espace (tiret, slash et souligné permis)")
        self.efOperateurs = Pmw.EntryField(self.fOpe, validate = {"max" : 20, "maxstrict" : False})
        self.efOperateurs.component('entry').config(width = 21)
        self.efOperateurs.grid(row = vLigne, column = 3, sticky = E+W)
        self.cbStatut = Commun.comboWidget(self.root, self.fOpe, self.root.cfgListe['Statut'])
        self.cbStatut.component('entryfield_entry').config(width = 13)
        self.cbStatut.grid(row = vLigne, column = 4, sticky = W+E)
        self.efLocalis = Pmw.EntryField(self.fOpe, validate = {"max" : 20, "maxstrict" : False})
        self.efLocalis.component('entry').config(width = 21)
        self.efLocalis.grid(row = vLigne, column = 5, sticky = E+W)
        self.efPosX = Pmw.EntryField(self.fOpe, validate = {"max" : 12, "maxstrict" : False})
        self.efPosX.component('entry').config(width = 13)
        self.efPosX.grid(row = vLigne, column = 6, sticky = E+W)
        self.efPosY = Pmw.EntryField(self.fOpe, validate = {"max" : 12, "maxstrict" : False})
        self.efPosY.component('entry').config(width = 13)
        self.efPosY.grid(row = vLigne, column = 7, sticky = E+W)
        self.efComment = Pmw.EntryField(self.fOpe, validate = {"max" : 30, "maxstrict" : False})
        self.efComment.component('entry').config(width = 31)
        self.efComment.grid(row = vLigne, column = 8, columnspan = 2, sticky = E+W)

        vLigne += 1

        Button (self.fOpe, text = "Valider", width = 14, command = self.valider, fg = "red", underline=0).grid (row = vLigne, column = 3)
        Button (self.fOpe, text = "Annuler", width = 14, command = self.annuler, fg = "red", underline=1).grid (row = vLigne, column = 5)
        
        self.root.printMenu.add_command(label="Réseau", command=self.imprimer)
#

    def initChamps(self):
        
        self.vous.set(self.root.userData['INDICATIF'] + " pour " + self.root.userData['INTITULE']) # Indicatif station
		
        self.lbListe.delete(0, END)
        for i in range (1,15):
            if self.root.netData["STATION"+str(i)].strip() == "":continue
            vXY = self.root.netData["COORD_XY_"+str(i)].split(',')
            Ligne = self.root.netData["STATION"+str(i)].ljust(8)+"  "+\
                    self.root.netData["TACTIC"+str(i)].ljust(12)+"  "+\
                    self.root.netData["OPERATEUR"+str(i)].ljust(20)+"  "+\
                    self.root.netData["STATUT"+str(i)].ljust(12)+"  "+\
                    self.root.netData["LOCAL"+str(i)].ljust(20)+"  "+\
                    vXY[0].ljust(12)+"  "+\
                    vXY[1].ljust(12)+"  "+\
                    self.root.netData["COMMENT"+str(i)].ljust(30)

            self.lbListe.insert(END, Ligne)
            # Couleur du fond des contrôles
            if self.lbListe.size()%2 == 0 :self.lbListe.itemconfig(END, bg = 'lightgray')

#
    def selectTab(self):
        self.initChamps()

        self.root.bind('<Alt-t>', self.ajouterStation)
        self.root.bind('<Alt-o>', self.modifier)
        self.root.bind('<Alt-s>', self.supprimer)

        #
        
    def unSelectTab(self):
        self.root.unbind('<Alt-t>')
        self.root.unbind('<Alt-o>')
        self.root.unbind('<Alt-s>')
        #
        
    def select(self, event=None):

        try:
            self.num.set(int(self.lbListe.curselection()[0]) + 1)
        except:
            self.num.set(0)
        
        
    def fOpeShow(self):
        
        self.lbListe.config(state=DISABLED)
        self.pbAjouter.configure(state=DISABLED)
        self.pbModifier.configure(state=DISABLED)
        self.pbSupprimer.configure(state=DISABLED)
        self.fOpe.grid()
        self.root.bind('<Alt-v>', self.valider)
        self.root.bind('<Return>', self.valider)
        self.root.bind('<Alt-n>', self.annuler)
        self.root.bind('<Escape>', self.annuler)
        
        self.efIndicatif.component('entry').focus_set()
    

    def fOpeHide(self):
    
        self.lbListe.config(state=NORMAL)
        self.pbAjouter.configure(state=NORMAL)
        self.pbModifier.configure(state=NORMAL)
        self.pbSupprimer.configure(state=NORMAL)
        self.fOpe.grid_remove()
        self.root.unbind('<Alt-v>')
        self.root.unbind('<Alt-e>')
        self.lbListe.focus_set()
        self.num.set(0)
        
    
    def ajouterStation(self, event=None):
        
        self.num.set(self.lbListe.size()+1)

        if int(self.num.get()) > 14:
            tkMessageBox.showinfo('Gestion du Réseau', 'Liste limitée à 14 indicatifs')
            return
        self.efIndicatif.setvalue("")
        self.efTactic.setvalue("")
        self.efOperateurs.setvalue("")
        self.cbStatut.selectitem(0, setentry = 1)
        self.efLocalis.setvalue("")
        self.efPosX.setvalue("")
        self.efPosY.setvalue("")
        self.efComment.setvalue("")
        self.fOpeShow()
        

    def modifier(self, event=None):

        i = self.num.get() 
        if i == 0: return
        self.efIndicatif.setvalue(self.root.netData["STATION"+str(i)])
        self.efTactic.setvalue(self.root.netData["TACTIC"+str(i)])
        self.efOperateurs.setvalue(self.root.netData["OPERATEUR"+str(i)])
        index = self.root.cfgListe['Statut'].index(self.root.netData["STATUT"+str(i)])
        self.cbStatut.selectitem(index, setentry = 1)
        self.efLocalis.setvalue(self.root.netData["LOCAL"+str(i)])
        vXY = self.root.netData["COORD_XY_"+str(i)].split(',')
        self.efPosX.setvalue(vXY[0])
        self.efPosY.setvalue(vXY[1])
        self.efComment.setvalue(self.root.netData["COMMENT"+str(i)])
        self.fOpeShow()
        

    def supprimer(self, event=None):
        
        debut = self.num.get()
        fin   = 14 # self.lbListe.index(END)
        
        if debut == 0: 
            return
        else:
            vMsg = "Voulez-vous supprimer la station " +self.root.netData["STATION"+str(debut)] + " ?"
            if tkMessageBox.askquestion("Gestion du Réseau", vMsg) != "yes" : return

        for i in range(debut, fin):
            if (i+1) > fin: break
            self.root.netData["STATION"+str(i)]   = self.root.netData["STATION"+str(i+1)]
            self.root.netData["TACTIC"+str(i)]    = self.root.netData["TACTIC"+str(i+1)]
            self.root.netData["OPERATEUR"+str(i)] = self.root.netData["OPERATEUR"+str(i+1)]
            self.root.netData["STATUT"+str(i)]    = self.root.netData["STATUT"+str(i+1)]
            self.root.netData["LOCAL"+str(i)]     = self.root.netData["LOCAL"+str(i+1)]
            self.root.netData["COORD_XY_"+str(i)] = self.root.netData["COORD_XY_"+str(i+1)]
            self.root.netData["COMMENT"+str(i)]   = self.root.netData["COMMENT"+str(i+1)]
            
        self.root.netData["STATION"+str(fin)] = ""
        self.root.netData["TACTIC"+str(fin)] = ""
        self.root.netData["OPERATEUR"+str(fin)] = ""
        self.root.netData["STATUT"+str(fin)] = "Inactif"
        self.root.netData["LOCAL"+str(fin)] = ""
        self.root.netData["COORD_XY_"+str(fin)] = ","
        self.root.netData["COMMENT"+str(fin)] = ""
        
        writeReseau(self)

        self.initChamps()
        self.fOpeHide()


    def annuler(self, event=None):
        self.fOpeHide()
        self.lbListe.selection_clear(ACTIVE)
        
    def valider(self, event=None):

        # Appliquer les modifs dans le dictionnaire des stations du réseau
        i = self.num.get()
        self.root.netData["STATION"+str(i)] = self.efIndicatif.getvalue().upper()
        self.root.netData["TACTIC"+str(i)] = self.efTactic.getvalue().upper()
        self.root.netData["OPERATEUR"+str(i)] = self.efOperateurs.getvalue()
        self.root.netData["STATUT"+str(i)] = self.cbStatut.get()
        self.root.netData["LOCAL"+str(i)] = self.efLocalis.getvalue()
        self.root.netData["COORD_XY_"+str(i)] = self.efPosX.getvalue()+","+self.efPosY.getvalue()
        self.root.netData["COMMENT"+str(i)] = self.efComment.getvalue()
     
        # Enregistrer les modifs dans le fichier de session
        writeReseau(self)

        # Déverrouiller la liste avant mise à jour
        self.lbListe.config(state=NORMAL)
        self.initChamps()

        # Masquer la frame de saisie
        self.fOpeHide()
# 

    def swap(self, sens):
        if self.lbListe.curselection() == ():return
        i = int(self.lbListe.curselection()[0])
        if sens == "-" and i == 0:return
        if sens == "+" and i == self.lbListe.index(END):return
        
        ligne = self.lbListe.get(i)
        aspect = self.lbListe.itemcget(i, 'background')
        self.lbListe.delete(i)
        if i%2 == 0 :self.lbListe.itemconfig(i, bg = 'lightgray')
        if sens == "-":
            i -= 1
        else:
            i += 1
        self.lbListe.insert(i, ligne)
        if i%2 == 0 :self.lbListe.itemconfig(i, bg = 'lightgray')
        self.lbListe.selection_set(i)
        
            
    def imprimer(self):

        vAlerte = self.root.userData['ACTIVATION']
        # Nom du fichier
        self.vFic = Commun.getFicREZO(self.root)+".TXT"
        vNb = 1
        
        fic = open(Commun.getFullPath(self.root, self.vFic),'w')
        fic.write(self.vFic+"\n\n")
        fic.write('################################################################################\n')
        fic.write('- ' +(vAlerte + ' - ')*3+'\n')
        fic.write('--------------------------------------------------------------------------------\n')

        # Informations transmission
        fic.write(("COMPOSITION DU RESEAU " + self.root.userData['SERVICE']).center(80)+"\n")
        fic.write('================================================================================\n')

        # Entête du message
        fic.write("Station directrice  : " + self.root.userData['INDICATIF'] + "\n")
        fic.write("Cadre de la mission : " + self.root.userData['INTITULE'] + "\n")
        fic.write('--------------------------------------------------------------------------------\n')

        # Corps du message
        for i in range(1,15):
            if self.root.netData["STATION"+str(i)] != "" :
                fic.write("Station N° " + str(i) +"\n")
                fic.write("        Indicatif      : " + Commun.encode(self.root.netData["STATION"+str(i)]))
                fic.write("        Alias Tactique : " + Commun.encode(self.root.netData["TACTIC"+str(i)]) + "\n")
                fic.write("        Opérateur(s)   : " + Commun.encode(self.root.netData["OPERATEUR"+str(i)]) + "\n")
                fic.write("        Statut         : " + Commun.encode(self.root.netData["STATUT"+str(i)]) + "\n")
                fic.write("        Localisation   : " + Commun.encode(self.root.netData["LOCAL"+str(i)]) + "\n")
                fic.write("        Position       : " + Commun.encode(self.root.netData["COORD_XY_"+str(i)]) + "\n")
                fic.write("        Commentaire    : " + Commun.encode(self.root.netData["COMMENT"+str(i)]) + "\n")
                fic.write("\n")
                vNb += 1
        fic.write('--------------------------------------------------------------------------------\n')

        # Final du message
        fic.write("Nombre de stations  : " + str(vNb) + "\n")
        fic.write("GDH édition         : " + datetime.datetime.now().strftime("%d/%m/%y %H:%M") + "\n")
        fic.write('================================================================================\n')
        fic.write('- ' +(vAlerte + ' - ')*3+'\n')
        fic.write('################################################################################\n')

        fic.close()

        # Impression
        if self.root.userData['IMPR_LOG'] == "OUI" :
            os.startfile(Commun.getFullPath(self.root,self.vFic), "print")
        else :
            tkMessageBox.showinfo('Gestion du Réseau', 'Rapport créé : ' + self.vFic)
        
        self.vFen.focus_set()
#
def writeReseau(self):
    """Sauvegarde des paramètres de session""" 
    vData = []
    for cle, valeur in self.root.netData.items():
        vData.append(cle + " = " + valeur +"\n")
    fic = open(Commun.getFullPath(self.root,Commun.getFicReseau(self.root)), 'w')
    fic.writelines(vData)
    fic.close()
#
