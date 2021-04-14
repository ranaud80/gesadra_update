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

###################### Gestion de la main courante.
class FormMCI:
    """Classe d�finissant la fen�tre Main Courante Informatique"""

    def __init__(self, appli):
        """Constructeur de l'onglet Mci"""

        self.root      = appli # R�f�rence � l'application racine
        self.fenetre   = self.root.notebook.add('Main Courante du Trafic')

        self.boutonE   = [] # liste des boutons EMETTEURS
        self.boutonR   = [] # liste des boutons RECEPTEURS
        self.boutonMsg = [] # liste des boutons MESSAGES
        
        # Chargement des dictionnaires
        self.fgCol = self.root.cfgListe['fgUrg']
        self.bgCol = self.root.cfgListe['bgUrg']

        # Composants de la fen�tre
        self.drawMCI()
        self.bulleAide()

        # Alimentation de la liste
        self.razSaisie()
        self.alimListe()

        # Gestion des raccourcis clavier
        self.selectTab()


    def drawMCI(self):
        # variables locales
        vLigne = 1 # N� de ligne pour le positionnement des composants

        # Composants de la fen�tre
        vFen = self.fenetre
        # Liste des stations du r�seau
        Label (vFen,text = "Stations pr�sentes sur le r�seau", fg = "blue",bg = "orange").grid(row = vLigne, column = 0,columnspan = 16, sticky = E+W)
        vLigne += 1
        # 14 boutons "Emetteur" (le bouton z�ro "Tous" est supprim� � la construction)
        Label (vFen, text = "Re�u de :").grid(row = vLigne, column = 0)
        for i in range(0,15): 
            self._drawBoutonE (i, i+1, vLigne)
        vLigne += 1
        
        # 15 boutons "Destinataires" (14 + "Tous")
        Label (vFen, text = "Emis vers :").grid(row = vLigne, column = 0)
        for i in range(0, 15):
            self._drawBoutonD (i, i+1, vLigne)
        vLigne += 1
		
		#ajout d'une ligne "Emetteur & recepteur"
		
		# 15 boutons "Emetteur" suivants
        Label (vFen, text = "Re�u de :").grid(row = vLigne, column = 0)
        for i in range(0,15): 
            self._drawBoutonE (i+15, i+1, vLigne)
        vLigne += 1
        
        # 15 boutons "Destinataires" suivants
        Label (vFen, text = "Emis vers :").grid(row = vLigne, column = 0)
        for i in range(0, 15):
            self._drawBoutonD (i+15, i+1, vLigne)
        vLigne += 1
		#fin
		
		
		
        # Donn�es du trafic
        Label (vFen,text = "Informations transmises", fg = "blue",bg = "orange").grid(row = vLigne, column = 0, columnspan = 16, sticky = E+W)
        vLigne += 1
        # Frame (� droite) des messages pr�d�finis
        self.fBtn = LabelFrame(vFen, bd = 2, text = " Messages pr�d�finis ", fg = "blue")
        self.fBtn.grid(row = vLigne, column = 10, rowspan = 5, columnspan = 6)
        self._drawBoutonMSG(0, vLigne, 0)
        self._drawBoutonMSG(1, vLigne, 1)
        self._drawBoutonMSG(2, vLigne, 2)
        self._drawBoutonMSG(3, vLigne+1, 0)
        self._drawBoutonMSG(4, vLigne+1, 1)
        self._drawBoutonMSG(5, vLigne+1, 2)
        self._drawBoutonMSG(6, vLigne+2, 0)
        self._drawBoutonMSG(7, vLigne+2, 1)
        self._drawBoutonMSG(8, vLigne+2, 2)
        # Contr�les standards
        Label (vFen, text = "Groupe Date/Heure : " ).grid( row = vLigne, column = 0, sticky = W)
        self.efGdh = Commun.gdhWidget(self.root, vFen)
        self.efGdh.grid(row = vLigne, column = 1, columnspan = 2, sticky = W)
        self.bGdh = Button(vFen, width = 8, bd = 1, fg = "blue", text = "Forcer", command = self.forcerGDH, underline = 1)
        self.bGdh.grid(row = vLigne, column = 3)
        vLigne += 1
        Label (vFen, text = "De (Emetteur) : " ).grid( row = vLigne, column = 0,columnspan = 1, sticky = W)
        self.efEmetteur = Pmw.EntryField (vFen, validate = {"validator" : Commun.indicatifValidator, "min" : 2, "max" : 8, "minstrict" : False, "maxstrict" : False})
        self.efEmetteur.component('entry').bind('<Key>', Commun.uppercaseKey)
        self.efEmetteur.grid (row = vLigne,column = 1, columnspan = 2, sticky = W)
        Label ( vFen, text = "A (Destinataire) : " ).grid( row = vLigne, column = 4,columnspan = 2, sticky = W)
        self.efDestinataire = Pmw.EntryField (vFen, validate = {"validator" : Commun.indicatifValidator, "min" : 2, "max" : 8, "minstrict" : False, "maxstrict" : False})
        self.efDestinataire.component('entry').bind('<Key>', Commun.uppercaseKey)
        self.efDestinataire.grid (row = vLigne, column = 6, columnspan = 2, sticky = W)
        vLigne += 1
        Label (vFen, text = "Degr� d'urgence : " ).grid( row = vLigne, column = 0, columnspan = 2, sticky = W)
        self.cbDegUrg = Commun.comboWidget(self.root, vFen, self.root.cfgListe['DegUrg'])
        self.cbDegUrg.grid(row = vLigne, column = 1, columnspan = 3, sticky = W)
        Label (vFen, text = "Transmis en : " ).grid( row = vLigne, column = 4, columnspan = 2, sticky = W)
        self.cbMoyTrans = Commun.comboWidget(self.root, vFen, self.root.cfgListe['Moyen_RX'])
        self.cbMoyTrans.grid(row = vLigne, column = 6, columnspan = 3, rowspan = 1,  sticky = W)
        vLigne += 1
        Label (vFen, text = "Texte du message : " ).grid( row = vLigne, column = 0,columnspan = 2, sticky = W)
        self.efTexte = Pmw.EntryField (vFen, validate = {"min" : 1, "max" : 80, "minstrict" : False, "maxstrict" : False})
        self.efTexte.grid(row = vLigne, column = 1, columnspan = 9, sticky = E+W)
        vLigne += 1
        
        self.bValider = Button (vFen, text = "Valider", command = self.validerMCI, fg = "red", underline = 0)
        self.bValider.grid(row = vLigne, column = 1, columnspan = 2, sticky = E+W, padx = 5,pady = 5 )
        self.bEffacer = Button (vFen, text = "Effacer", command = self.effacerMCI, fg = "red", underline = 0)
        self.bEffacer.grid(row = vLigne, column = 4, columnspan = 2, sticky = E+W, padx = 5,pady = 5)
        self.bQuitter = Button (vFen, text = "Quitter", command = self.quitterMCI, fg = "red", underline = 0)
        self.bQuitter.grid(row = vLigne, column = 7, columnspan = 2, sticky = E+W, padx = 5,pady = 5)
        vLigne += 1

        # Derni�res infos de la vacation
        Label (vFen,text = "                         de :                        � :                                                                       Derni�res transmissions enregistr�es", fg = "blue",bg = "orange").grid( row = vLigne, column = 0, columnspan = 16, sticky = W)
        vLigne += 1
        fLog = Frame(vFen)
        fLog.grid(row = vLigne, column = 0, columnspan = 16)
        sbListe = Scrollbar(fLog, orient = VERTICAL)
        self.lbListe = Listbox(fLog, height = 13, width = 140, font = self.root.fonteFixe, yscrollcommand = sbListe.set)
        self.lbListe.grid(row = vLigne, column = 0, sticky = E+W)
        sbListe.config(command = self.lbListe.yview)
        sbListe.grid(row = vLigne, column = 1, sticky = N+S)
    #
    def _drawBoutonE (self, indice, colonne, ligne):
        bouton = Button(self.fenetre, width = 8, foreground = "#ff0000", takefocus = 1)
        bouton.config(command = lambda x = indice : self.cliquerRecuDe(x))
        bouton.grid(column = colonne, row = ligne, sticky = E+W)
        if indice == 0: bouton.grid_remove() # Suppression du bouton 0 "Tous"
        self.boutonE.append(bouton)
    #        
    def _drawBoutonD (self, indice, colonne, ligne):
        bouton = Button(self.fenetre, width = 8, foreground = "#009900", takefocus = 1)
        bouton.config(command = lambda x = indice : self.cliquerEmisVers(x))
        bouton.grid(column = colonne, row = ligne, sticky = E+W)
        if indice == 0: bouton.config(text = "TOUS") # Initialisation du bouton 0 "Tous"
        self.boutonR.append(bouton)
    #
    def initBoutons(self):
    
        for i in range(1,29):
            indicatif = self.root.netData["STATION"+str(i)]
            vBulle = self.root.netData["OPERATEUR"+str(i)]+"\n("+self.root.netData["STATUT"+str(i)]+")"
            self.boutonE[i].config(text = indicatif)
            self.boutonR[i].config(text = indicatif)
            self.root.bulle.bind(self.boutonE[i], vBulle.strip())
            self.root.bulle.bind(self.boutonR[i], vBulle.strip())
    #
            
    def _drawBoutonMSG (self, indice, ligne, colonne):
        vTexte = self.root.cfgListe["Msg"+str(indice)][0]
        bMsg = Button(self.fBtn, text = vTexte, width = 15, fg = "blue")
        bMsg.config(command = lambda x = indice : self.cliquerMessage(x))
        bMsg.grid(row = ligne, column = colonne, sticky = E+W, padx = 5, pady = 3)
        self.root.bulle.bind(bMsg, self.root.cfgListe["Msg"+str(indice)][1])
    #    
    # D�finition des bulles d'aide sur la fen�tre
    def bulleAide(self):
        # ATTENTION, les messages d'aide des Widgets GesADRA sont d�j� g�r�s
        self.root.bulle.bind(self.efEmetteur, "Indicatif de 2 � 8 car., sans espace (tiret, slash et soulign� permis)")
        self.root.bulle.bind(self.efDestinataire, "Indicatif de 2 � 8 car., sans espace (tiret, slash et soulign� permis)")
        self.root.bulle.bind(self.efTexte, "Contenu du message, de 1 � 80 car.")
    #    
    # Action sur un bouton "Emetteur"
    def cliquerRecuDe(self, indice):
        # Calcul du GDH, insertion des indicatifs et positionnement sur le texte � saisir
        # Contr�le de l'indicatif 
        indicatif = self.controleIndicatif(indice)
        if indicatif != "":
            # Alimentation des donn�es MCI
            self.razSaisie()
            vGdh = datetime.datetime.now().strftime("%d/%m/%y %H:%M")
            self.efGdh.setvalue(vGdh)
            self.efEmetteur.setvalue(indicatif)
            self.efDestinataire.setvalue(self.root.userData['INDICATIF'])
            self.efTexte.component('entry').focus_set()
        else :
            self.fenetre.focus_set()
            
    # Action sur un bouton "Emetteur"
    # Calcul du GDH, insertion des indicatifs et positionnement sur le texte � saisir
    def cliquerEmisVers(self, indice):
        # Contr�le de l'indicatif 
        indicatif = self.controleIndicatif(indice)
        if indicatif != "":
            # Alimentation des donn�es MCI
            self.razSaisie()
            vGdh = datetime.datetime.now().strftime("%d/%m/%y %H:%M")
            self.efGdh.setvalue(vGdh)
            self.efEmetteur.setvalue(self.root.userData['INDICATIF'])
            self.efDestinataire.setvalue(indicatif)
            self.efTexte.component('entry').focus_set()
        else :
            self.fenetre.focus_set()

    # Contr�le de l'indicatif et saisie si absent
    def controleIndicatif (self, indice, message=None):
        # Message par d�faut
        if message == None : message = "Nouvel indicatif :"
        # Si l'indicatif n'est pas dans le dictionnaire R�seau, on demande sa saisie
        indicatif = self.root.netData["STATION"+str(indice)]
        if indicatif == "" :
           indicatif = tkSimpleDialog.askstring("Gestion du R�seau", message)
           # Si pas de saisie, on rend la main
           if indicatif == None: return ""
           # Contr�le par le validateur
           if Commun.indicatif3Validator(indicatif) == Pmw.OK :
               # Saisie correcte
               indicatif = indicatif.upper()
               self.root.netData["STATION"+str(indice)] = indicatif
               self.root.netData["STATUT"+str(indice)] = "Actif"
               vBulle = self.root.netData["OPERATEUR"+str(indice)]+"\n("+self.root.netData["STATUT"+str(indice)]+")"
               self.root.bulle.bind(self.boutonE[indice], vBulle.strip())               
               self.root.bulle.bind(self.boutonR[indice], vBulle.strip())               
               self.boutonE[indice].config(text = indicatif)
               self.boutonR[indice].config(text = indicatif)
           else :
               # Erreur : relancer le contr�le de l'indicatif (r�cursivit�)
               indicatif = self.controleIndicatif (indice, "Saisie incorrecte : l'indicatif doit �tre de 2 � 8 car.,\n" +
                                                           "sans accent ni espace (tiret, slash et soulign� permis) :")
               
        return indicatif
    
    # Action sur un bouton "Forcer GDH"
    def forcerGDH(self, evt = None):
        vGdh = datetime.datetime.now().strftime("%d/%m/%y %H:%M")
        self.efGdh.setvalue(vGdh)

    # Action sur un bouton "Message"
    # Calcul du GDH, insertion des indicatifs et positionnement sur le texte � saisir
    def cliquerMessage(self, indice):
        # Contr�le du bouton 
        try:
            vLibelle = self.root.cfgListe["Msg"+str(indice)][0]
        except:
            return None
        # Alimentation des donn�es MCI
        vTexte = self.root.cfgListe["Msg"+str(indice)][1]
        self.efTexte.setvalue(str(vTexte))
        self.efTexte.component('entry').focus_set()
        # S'il n'y a pas de troisi�me param�tre : on valide
        try:
            vVariable = self.root.cfgListe["Msg"+str(indice)][2]
        except:
            self.validerMCI(self)

    # Action sur un bouton "Valider"
    def validerMCI(self, evt = None):
        """Traitement du bouton 'Valider'"""
        # Contr�le de la validit� des donn�es
        if self.controleSaisie() == False: return None

        # Ligne de MCI    
        infosMCI = Commun.InfosMCI(self.efGdh.getvalue(), self.efEmetteur.getvalue(), self.efDestinataire.getvalue(), \
                                   self.cbDegUrg.get(), self.cbMoyTrans.get(), self.efTexte.getvalue())
        infosMCI.ecrire(self.root)

        # Remise � Z�ro du formulaire
        self.razSaisie()

        
    # Action sur le bouton "Effacer"
    def effacerMCI(self, evt = None):
        """Traitement du bouton 'Effacer'"""
        # Remise � Z�ro de la saisie
        self.razSaisie()

        
    # Action sur le bouton "Quitter"
    def quitterMCI(self, evt = None):
        """Traitement du bouton 'Quitter'"""
        if self.efGdh.getvalue().strip() != "":
            etesVousSur = tkMessageBox.askquestion('Main Courante du Trafic', \
                                                   "Saisie en cours.\nConfirmez-vous la fermeture de cet onglet ?")
        else:
            etesVousSur = "yes"
            
        if etesVousSur == "yes" :
            self.root.printMenu.delete(self.root.printMenu.index("Main Courante"))
            self.unSelectTab()
            self.root.notebook.delete('Main Courante du Trafic')
            self.root.fenMCI = None 
            self.fenetre.destroy()
        else:
            self.fenetre.focus_set()

    def imprimerMCI(self, evt = None):
        """Traitement du bouton 'Quitter'"""
        return
        
    def createTab(self):
        self.root.printMenu.add_command(label="Main Courante", command=self.imprimerMCI)
    #
    
    def selectTab(self):
        self.initBoutons()

        # self.lbListe.bind("<Double-1>", self.majLigne)
        self.root.bind('<Alt-o>', self.forcerGDH)
        self.root.bind('<Alt-v>', self.validerMCI)
        self.root.bind('<Return>', self.validerMCI)
        self.root.bind('<Alt-e>', self.effacerMCI)
        self.root.bind('<Escape>', self.effacerMCI)
        self.root.bind('<Alt-q>', self.quitterMCI)
    #
        
    def unSelectTab(self):

        # self.lbListe.unbind("<Double-1>", self.majLigne)
        self.root.unbind('<Alt-o>')
        self.root.unbind('<Alt-v>')
        self.root.unbind('<Return>')
        self.root.unbind('<Alt-e>')
        self.root.unbind('<Escape>')
        self.root.unbind('<Alt-q>')
    #
        
    # Remise � z�ro de la saisie utilisateur
    def razSaisie(self):
        self.efGdh.setvalue("")
        self.efEmetteur.setvalue("")
        self.efDestinataire.setvalue("")
        self.cbDegUrg.selectitem(0)
        self.cbMoyTrans.selectitem(0)
        self.efTexte.setvalue("")

    # Validation de la saisie utilisateur
    def controleSaisie(self):
        #Contr�le de saisie
        if self.efGdh.valid() == False or \
           self.efEmetteur.valid() == False or \
           self.efDestinataire.valid() == False or \
           self.efTexte.valid() == False :
            tkMessageBox.showwarning('Contr�le', 'Les champs en rouge sont absents ou incorrects')
            self.fenetre.focus_set()
            return False
        
        if self.efTexte.getvalue().strip() == "":
            tkMessageBox.showwarning('Contr�le', 'Texte vide')
            self.efTexte.component('entry').focus_set()
            return False

        return True

        
    # Affichage de la ligne dans la list-box
    def afficherListe(self, infosMCI):

        # Insertion de la ligne en t�te de liste
        self.lbListe.insert('0', infosMCI.getLigne(self.root))
        self.lbListe.see('0')

        # Coloration en fonction du Degr� d'Urgence
        vIndex = self.root.cfgListe['DegUrg'].index(infosMCI.getUrg())
        self.lbListe.itemconfig('0', fg = self.fgCol[vIndex])
        self.lbListe.itemconfig('0', bg = self.bgCol[vIndex])


    # Affichage de la ligne dans la list-box
    def majLigne(self, event=None):
        tkMessageBox.showinfo('Contr�le', 'Mise � jour de la ligne ' + self.lbListe.curselection()[0])
        self.fenetre.focus_set()

            
    # Alimentation de la liste depuis le fichier de log
    def alimListe (self):

        try:
            fic = open (Commun.getFullPath(self.root, Commun.getFicMCI(self.root)),'r')
        except IOError:
            return
        
        entete = fic.readline() # L'ent�te est la premi�re ligne du fichier : on n'en fait rien
        
        for line in fic.readlines():
            vData = line.split(';')
            vHeure = vData[0].split (" ")
            # Extraction et mise en forme des donn�es
            vLigne = " " + vHeure[1].ljust(5)+" | " + vData[2].ljust(10)+" | " + \
                     vData[3].ljust(10)+" | " + vData[4].ljust(17)+" | " + vData[5].rstrip("\n")
            self.lbListe.insert('0', vLigne)
            # Colorisation de la ligne
            try:
                vIndex = self.root.cfgListe['DegUrg'].index(vData[4])
                self.lbListe.itemconfig('0', fg = self.fgCol[vIndex])
                self.lbListe.itemconfig('0', bg = self.bgCol[vIndex])
            except ValueError:
                True
                
        fic.close()

        # Positionner la liste sur la premi�re ligne
        self.lbListe.see('0')
       