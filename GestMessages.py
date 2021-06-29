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

###################### Gestion des messages
class FormGMsg:
    """Classe définissant la fenêtre Gestion des Messages"""

    def __init__(self, appli, onglet):
        """Constructeur de la fenêtre GMsg"""

        # variables locales
        vLigne = 1 # N° de ligne pour le positionnement des composants
        vIndice = 0

        # Référence sur la fenêtre appelante
        self.root = appli
        self.fenetre = onglet

        # Composants de la fenêtre
        # Liste des stations du réseau
        Label (fenetre,text = "Stations présentes sur le réseau", fg = "blue",bg = "orange").grid(row = vLigne, column = 0,columnspan = 12, sticky = E+W)
        vLigne += 1
        # 10 boutons "Emetteur"
        Label (fenetre, text = "Reçu de :").grid(row = vLigne, column = 1)
        for i in range(10): 
            vIndice = i+1  # N° de bouton (i commence à 0)
            vColonne = i+2 # Positionnement 
            self.dessinerBoutonE (vIndice, vColonne, vLigne, appli)
        vLigne += 1
        # 10 boutons "Destinataires"
        Label (fenetre, text = "Emis vers :").grid(row = vLigne, column = 1)
        for i in range(10):
            vIndice = i+1  # N° de bouton (i commence à 0)
            vColonne = i+2 # Positionnement 
            self.dessinerBoutonD (vIndice, vColonne, vLigne, appli)
        vLigne += 1

        # Données du trafic
        Label (fenetre,text = "Informations transmises", fg = "blue",bg = "orange").grid( row = vLigne, column = 0, columnspan = 12, sticky = E+W)
        vLigne += 1
        Label (fenetre, text = "Groupe Date/Heure : " ).grid( row = vLigne, column = 1, sticky = W )
        self.eGdh = Entry (fenetre)
        self.eGdh.grid(row = vLigne, column = 2, columnspan = 2, sticky = W)
        self.bGdh = Button(self.fenetre, width = 8, bd = 1, fg = "blue", text = "Forcer")
        self.bGdh.grid(row = vLigne, column = 4)
        self.bGdh.configure(command = self.forcerGDH)
        vLigne += 1
        Label (fenetre, text = "De (Emetteur (AO)) : " ).grid( row = vLigne, column = 1, sticky = W )
        self.eEmetteur = Entry (fenetre)
        self.eEmetteur.grid ( row = vLigne,column = 2, columnspan = 2, sticky = W)
        Label ( fenetre, text = "A (Destinataire (AD)) : " ).grid( row = vLigne, column = 5,columnspan = 2, sticky = W )
        self.eDestinataire = Entry (fenetre)
        self.eDestinataire.grid ( row = vLigne,column = 7, columnspan = 2, sticky = W)
        vLigne += 1
        Label (fenetre, text = "Degré d'urgence : " ).grid( row = vLigne, column = 1,columnspan = 2, sticky = W )
        self.cbUrg = Pmw.ComboBox(fenetre, scrolledlist_items = appli.cfgListe['DegUrg'], listheight = 80, history = 0)
        self.cbUrg.selectitem(0)
        self.cbUrg.grid ( row = vLigne, column = 2, columnspan = 3, sticky = W )
        Label (fenetre, text = "Transmis en : " ).grid( row = vLigne, column = 5,columnspan = 2, sticky = W )
        self.cbMoyTrans = Pmw.ComboBox ( fenetre, scrolledlist_items = appli.cfgListe['Moyen_RX'], listheight = 80, history = 0)
        self.cbMoyTrans.selectitem(0)
        self.cbMoyTrans.grid ( row = vLigne, column = 7, columnspan = 3, sticky = W )
        vLigne += 1
        Label ( fenetre, text = "Texte du message : " ).grid( row = vLigne, column = 1, columnspan = 2, sticky = W )
        self.eTexte = Entry(fenetre)
        self.eTexte.grid ( row = vLigne, column = 2, columnspan = 9, sticky = E+W )
        vLigne += 1
        self.bValider = Button (fenetre, text = "Valider", command = self.validerGMsg, fg = "red")
        self.bValider.grid ( row = vLigne, column = 2, columnspan = 2, sticky = E+W, padx = 5,pady = 5 )
        self.bEffacer = Button ( fenetre, text = "Effacer", command = self.effacerGMsg, fg = "red")
        self.bEffacer.grid ( row = vLigne, column = 5, columnspan = 2, sticky = E+W, padx = 5,pady = 5)
        self.bQuitter = Button ( fenetre, text = "Quitter", command = lambda :self.quitterGMsg(appli), fg = "red")
        self.bQuitter.grid ( row = vLigne, column = 8, columnspan = 2, sticky = E+W, padx = 5,pady = 5)
        vLigne += 1

        # Dernières infos de la vacation
        Label (fenetre,text = "Dernières transmissions enregistrées", fg = "blue",bg = "orange").grid( row = vLigne, column = 0, columnspan = 12, sticky = E+W)
        vLigne += 1
        self.lbListe = Listbox(fenetre, height = 10, font = appli.fonteFixe)
        self.lbListe.grid(row = vLigne, column = 0, columnspan = 12, sticky = E+W)

    def dessinerBoutonE (self, indice, colonne, ligne, appli):
        indicatif = appli.netData["STATION"+str(indice)]
        bouton = Button(self.fenetre, width = 8, foreground = "#ff0000", takefocus = 1, text = indicatif)
        bouton.grid(column = colonne, row = ligne, sticky = E+W)
        bouton.configure(command = lambda x = indice : self.cliquerRecuDe(x, appli))
        self.boutonE.append(bouton)
        
    def dessinerBoutonD (self, indice, colonne, ligne, appli):
        indicatif = appli.netData["STATION"+str(indice)]
        bouton = Button(self.fenetre, width = 8, foreground = "#009900", takefocus = 1, text = indicatif)
        bouton.grid(column = colonne, row = ligne, sticky = E+W)
        bouton.configure(command = lambda x = indice :self.cliquerEmisVers(x, appli))
        self.boutonR.append(bouton)
    
    # Action sur un bouton "Emetteur"
    # Calcul du GDH, insertion des indicatifs et positionnement sur le texte à saisir
    def cliquerRecuDe(self, indice, appli):
        # Contrôle de l'indicatif 
        indicatif = self.controleIndicatif(indice, appli)
        if indicatif == None: return
        # Alimentation des données GMsg
        self.razSaisie()
        vGdh = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        self.eGdh.insert(0, vGdh)
        self.eEmetteur.insert(0, indicatif)
        self.eDestinataire.insert(0, appli.userData['INDICATIF'])
        self.eTexte.focus_set()
            
    # Action sur un bouton "Emetteur"
    # Calcul du GDH, insertion des indicatifs et positionnement sur le texte à saisir
    def cliquerEmisVers(self, indice, appli):
        # Contrôle de l'indicatif 
        indicatif = self.controleIndicatif(indice, appli)
        if indicatif == None: return
        # Alimentation des données GMsg
        self.razSaisie()
        vGdh = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        self.eGdh.insert(0, vGdh)
        self.eEmetteur.insert(0,appli.userData['INDICATIF'])
        self.eDestinataire.insert(0, indicatif)
        self.eTexte.focus_set()

    # Contrôle de l'indicatif et saisie si absent
    def controleIndicatif (self, indice, appli):
        indicatif = appli.netData["STATION"+str(indice)]
        if indicatif == "" :
           indicatif = tkSimpleDialog.askstring("Gestion du Réseau", "Nouvel indicatif")
           if indicatif != None:
               indicatif = indicatif.upper()
               appli.netData["STATION"+str(indice)] = indicatif
               self.boutonE[indice].configure(text = indicatif)
               self.boutonR[indice].configure(text = indicatif)
        return indicatif
    
    # Action sur un bouton "Forcer GDH"
    def forcerGDH(self):
        vGdh = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        self.eGdh.delete(0, END)
        self.eGdh.insert(0, vGdh)

    # Action sur un bouton "Valider"
    def validerGMsg(self):
        """Traitement du bouton 'Valider'"""
        # variables locales
        vLigneInfo = ""

        #Contrôle de la validité des données
        if self.controleSaisie() == False:
            # Si erreur, on stoppe le traitement
            return None

        # Mise en forme de la ligne d'infos    
        vLigneInfo = self.creerLigneGMsg()
        # Ecriture dans le fichier
        self.ecrireGMsg(vLigneInfo)
        # Affichage dans la list-box
        self.afficherListe(vLigneInfo)

        # Remise à Zéro du formulaire
        self.razSaisie()

        
    # Action sur le bouton "Effacer"
    def effacerGMsg(self):
        """Traitement du bouton 'Effacer'"""
        # Remise à Zéro de la saisie
        self.razSaisie()


    # Action sur le bouton "Effacer"
    def quitterGMsg(self, appli):
        """Traitement du bouton 'Quitter'"""
        etesVousSur = tkMessageBox.askquestion("Fermeture de la Main Courante", \
                                               "Confirmez-vous la fermeture de la Main Courante ?")
        if etesVousSur == "yes" :
            appli.fenGMsg = None 
            self.fenetre.destroy()
        else:
            self.fenetre.focus_set()

    # Remise à zéro de la saisie utilisateur
    def razSaisie(self):
        self.eGdh.delete(0, END)
        self.eEmetteur.delete(0, END)
        self.eDestinataire.delete(0, END)
        self.cbUrg.selectitem(0)
        self.cbMoyTrans.selectitem(0)
        self.eTexte.delete(0, END)

    # Validation de la saisie utilisateur
    def controleSaisie(self):
        #Contrôle de saisie
        if self.eTexte.get().strip() == "":
            tkMessageBox.showwarning('Controle', 'Texte vide')
            return False

        return True
        
    # Insertion de la ligne dans le fichier Main Courante
    def ecrireGMsg(self, ligne):
        vFic = Commun.getFicMCI(appli)
        fic = open (Commun.getFullPath(appli, vFic),'a')
        fic.write(ligne+ "\n")
        fic.close()

    # Affichage des 10 dernières lignes dans la list-box
    def afficherListe(self, ligne):
        if self.lbListe.size() >= 10:
            self.lbListe.delete('0')

        vGdh = self.eGdh.get().split (" ")
        vLigne = " " + vGdh[1].ljust(5)+" | "+\
                 self.eEmetteur.get().ljust(10)+" | "+\
                 self.eDestinataire.get().ljust(10)+" | "+\
                 self.cbUrg.get().ljust(17)+" | "+\
                 self.eTexte.get()

        self.lbListe.insert('end', vLigne)

    # Creation d'une ligne de la main courante.
    def creerLigneGMsg(self):

        # Récupération des données saisies
        vGdh = self.eGdh.get()
        vEmetteur = self.eEmetteur.get()
        vDestinataire = self.eDestinataire.get()
        vUrg = self.cbUrg.get()
        vMoyTrans = self.cbMoyTrans.get()
        vTexte = self.eTexte.get()

        vLigneGMsg = vGdh+";"+vMoyTrans+";"+vEmetteur+";"+vDestinataire+";"+vUrg+";"+vTexte
        return vLigneGMsg
            
    def creerFicheInfo(self, appli):

        Transmetteur = appli.userData['INDICATIF']
        nomFichier2 = Transmetteur+'-GMsg-'+str(aujourdhui) +'-'+heure_courante2+'.txt'
        vAlerte = appli.userData['ACTIVATION']
        vService = appli.userData['SERVICE']

        fich = open ( nomFichier2, 'w' ) # on ouvre/cree le fichier si il existe deja, celui-ci est vide de ses informations...
        fich.write('####################################################################################################\n')
        fich.write(vAlerte + ' - ' + vAlerte + ' - ' + vAlerte + '\n')
        fich.write("\nFICHE DE COLLECTE DE RENSEIGNEMENTS PROVENANT DES DIFFERENTS SERVICES (DDE,SDIS,ddsp, etc ...) \n")
        fich.write("                    POUR ALIMENTATION DE LA MAIN COURANTE\n\n\n")
        fich.write("----------------------------------------------------------------------------------------------\n")
        fich.write("Appelant = "+encode (champ_Indicatif_Appelant.get())+"\n")
        fich.write("Appele = "+encode (champ_Indicatif_Appele.get())+"\n")
        fich.write("----------------------------------------------------------------------------------------------\n")
        fich.write("Groupe Date Heure (Réception) = "+encode (gdh_choix)+"          Service : "+ vService +"\n")
        fich.write("Moyen de réception de l'information : " + encode (comboMoyTrans.get()) + "\n")
        fich.write("----------------------------------------------------------------------------------------------\n")
        fich.write("Information à communiquer : " + encode (champ_texte.get())+"\n")
        fich.write("Transmetteur = "+encode (indicatif)+"\n")
        fich.write("FIN DE MESSAGE".center(80) + "\n")
        fich.write("\n" +  vAlerte + ' - ' + vAlerte + ' - ' + vAlerte + '\n')
        fich.write('####################################################################################################\n')
        fich.close()
   

        if impression == "OUI" :
            os.startfile(nomFichier2)
        else :
            imp = "non"
            
        
#Ouverture de la main courante dans le tableur#########################################
def ouvrirMainCourante():
    os.startfile(nomMainCourante)
