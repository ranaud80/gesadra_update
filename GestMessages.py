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
    """Classe d�finissant la fen�tre Gestion des Messages"""

    def __init__(self, appli, onglet):
        """Constructeur de la fen�tre GMsg"""

        # variables locales
        vLigne = 1 # N� de ligne pour le positionnement des composants
        vIndice = 0

        # R�f�rence sur la fen�tre appelante
        self.root = appli
        self.fenetre = onglet

        # Composants de la fen�tre
        # Liste des stations du r�seau
        Label (fenetre,text = "Stations pr�sentes sur le r�seau", fg = "blue",bg = "orange").grid(row = vLigne, column = 0,columnspan = 12, sticky = E+W)
        vLigne += 1
        # 10 boutons "Emetteur"
        Label (fenetre, text = "Re�u de :").grid(row = vLigne, column = 1)
        for i in range(10): 
            vIndice = i+1  # N� de bouton (i commence � 0)
            vColonne = i+2 # Positionnement 
            self.dessinerBoutonE (vIndice, vColonne, vLigne, appli)
        vLigne += 1
        # 10 boutons "Destinataires"
        Label (fenetre, text = "Emis vers :").grid(row = vLigne, column = 1)
        for i in range(10):
            vIndice = i+1  # N� de bouton (i commence � 0)
            vColonne = i+2 # Positionnement 
            self.dessinerBoutonD (vIndice, vColonne, vLigne, appli)
        vLigne += 1

        # Donn�es du trafic
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
        Label (fenetre, text = "Degr� d'urgence : " ).grid( row = vLigne, column = 1,columnspan = 2, sticky = W )
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

        # Derni�res infos de la vacation
        Label (fenetre,text = "Derni�res transmissions enregistr�es", fg = "blue",bg = "orange").grid( row = vLigne, column = 0, columnspan = 12, sticky = E+W)
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
    # Calcul du GDH, insertion des indicatifs et positionnement sur le texte � saisir
    def cliquerRecuDe(self, indice, appli):
        # Contr�le de l'indicatif 
        indicatif = self.controleIndicatif(indice, appli)
        if indicatif == None: return
        # Alimentation des donn�es GMsg
        self.razSaisie()
        vGdh = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        self.eGdh.insert(0, vGdh)
        self.eEmetteur.insert(0, indicatif)
        self.eDestinataire.insert(0, appli.userData['INDICATIF'])
        self.eTexte.focus_set()
            
    # Action sur un bouton "Emetteur"
    # Calcul du GDH, insertion des indicatifs et positionnement sur le texte � saisir
    def cliquerEmisVers(self, indice, appli):
        # Contr�le de l'indicatif 
        indicatif = self.controleIndicatif(indice, appli)
        if indicatif == None: return
        # Alimentation des donn�es GMsg
        self.razSaisie()
        vGdh = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        self.eGdh.insert(0, vGdh)
        self.eEmetteur.insert(0,appli.userData['INDICATIF'])
        self.eDestinataire.insert(0, indicatif)
        self.eTexte.focus_set()

    # Contr�le de l'indicatif et saisie si absent
    def controleIndicatif (self, indice, appli):
        indicatif = appli.netData["STATION"+str(indice)]
        if indicatif == "" :
           indicatif = tkSimpleDialog.askstring("Gestion du R�seau", "Nouvel indicatif")
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

        #Contr�le de la validit� des donn�es
        if self.controleSaisie() == False:
            # Si erreur, on stoppe le traitement
            return None

        # Mise en forme de la ligne d'infos    
        vLigneInfo = self.creerLigneGMsg()
        # Ecriture dans le fichier
        self.ecrireGMsg(vLigneInfo)
        # Affichage dans la list-box
        self.afficherListe(vLigneInfo)

        # Remise � Z�ro du formulaire
        self.razSaisie()

        
    # Action sur le bouton "Effacer"
    def effacerGMsg(self):
        """Traitement du bouton 'Effacer'"""
        # Remise � Z�ro de la saisie
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

    # Remise � z�ro de la saisie utilisateur
    def razSaisie(self):
        self.eGdh.delete(0, END)
        self.eEmetteur.delete(0, END)
        self.eDestinataire.delete(0, END)
        self.cbUrg.selectitem(0)
        self.cbMoyTrans.selectitem(0)
        self.eTexte.delete(0, END)

    # Validation de la saisie utilisateur
    def controleSaisie(self):
        #Contr�le de saisie
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

    # Affichage des 10 derni�res lignes dans la list-box
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

        # R�cup�ration des donn�es saisies
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
        fich.write("Groupe Date Heure (R�ception) = "+encode (gdh_choix)+"          Service : "+ vService +"\n")
        fich.write("Moyen de r�ception de l'information : " + encode (comboMoyTrans.get()) + "\n")
        fich.write("----------------------------------------------------------------------------------------------\n")
        fich.write("Information � communiquer : " + encode (champ_texte.get())+"\n")
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
