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


###################### Creation d'un message IARU.
class FormIARU:
    "Classe d�finissant le formulaire IARU"
    
    def __init__(self, appli):
        "Constructeur de la fen�tre IARU"

        self.root = appli # R�f�rence � l'application racine
        self.cAction = "" # Code Action ("", "R"eceiving, "S"ending, QS"P" Sending)

        # Cr�ation de la nouvelle fen�tre
        self.fenetre = Commun.nouvelleFenetre(self.root, "IARU Standard Message")
        # Fermeture par la case syst�me
        self.fenetre.protocol("WM_DELETE_WINDOW", self.quitterIARU)

        # Composants de la fen�tre
        self.dessineIARU()
        self.bulleAide()

        # Initialisations
        self.razSaisie()
        
        # Gestion des raccourcis clavier
        self.fenetre.bind('<Alt-v>', self.validerIARU)
        self.fenetre.bind('<Return>', self.validerIARU)
        self.fenetre.bind('<Alt-n>', self.annulerIARU)
        self.fenetre.bind('<Escape>', self.annulerIARU)
        self.fenetre.bind('<Alt-q>', self.quitterIARU)
        self.stText.bind('<Return>', self.noAction) # On ne valide pas par <Entr�e> sur la zone stText
        self.stText.bind('<Tab>', self.nextCtrl)
        self.stText.bind('<FocusOut>', self.countWords)


    def dessineIARU(self):

        # variables locales
        vLigne = 1 # N� de ligne pour le positionnement des composants
        vNomBouton = ""
        vIndice = 0
        vFen = self.fenetre

        # Composants de la fen�tre
        Label (vFen, text="IARU MESSAGE", fg="blue",bg="orange").grid(row=vLigne, column=0, columnspan=8, sticky=E+W)
        vLigne += 1

        self.btReceive = Button (vFen, text="Receiving", command = self.rcvIARU, fg="blue", underline = 0)
        self.btReceive.grid(row=vLigne, column=1, padx=5, pady=5, sticky = W+E)
        self.btSend = Button (vFen, text="Sending", command = self.senIARU, fg="blue", underline = 0)
        self.btSend.grid(row=vLigne, column=3, padx=5, pady=5, sticky = W+E)
        self.btQSP = Button (vFen, text="QSP Send/Receive", command = self.qspIARU, fg="blue", underline = 2)
        self.btQSP.grid(row=vLigne, column=5, padx=5, pady=5, sticky = W+E)
        vLigne += 1

        Label (vFen, text="Message Header", fg="blue",bg="cyan").grid(row=vLigne, column=0, columnspan=7, sticky=E+W)
        vLigne += 1
        Label (vFen, text="NUMBER").grid(row=vLigne, column=0, sticky = W+E)
        Label (vFen, text="PRECEDENCE").grid(row=vLigne, column=1, sticky = W+E)
        Label (vFen, text="STATION OF").grid(row=vLigne, column=2, sticky = W+E)
        Label (vFen, text="WORD COUNT").grid(row=vLigne, column=3, sticky = W+E)
        Label (vFen, text="PLACE OF ORIGIN").grid(row=vLigne, column=4, sticky = W+E)
        Label (vFen, text="FILING TIME").grid(row=vLigne, column=5, sticky = W+E)
        Label (vFen, text="FILING DATE").grid(row=vLigne, column=6, sticky = W+E)
        vLigne += 1
        Label (vFen, text="ORIGIN").grid(row=vLigne, column=2, sticky = W+E)
        Label (vFen, text="(Check)").grid(row=vLigne, column=3, sticky = W+E)
        vLigne += 1
        self.efNumber = Pmw.EntryField(vFen, validate=Commun.nonVideValidator)
        self.efNumber.component('entry').configure(justify="center")
        self.efNumber.grid (row = vLigne, column = 0, sticky = W)
        self.cbDegUrg = Commun.comboWidget (self.root, vFen, self.root.cfgListe['DegUrgIARU'])
        self.cbDegUrg.grid (row=vLigne, column=1, sticky = W)
        self.efStation = Pmw.EntryField (vFen, validate = {"validator" : Commun.indicatifValidator, "min" : 2, "max" : 8, "minstrict" : False, "maxstrict" : False})
        self.efStation.component('entry').bind('<Key>', Commun.uppercaseKey)
        self.efStation.grid (row = vLigne, column=2 ,sticky=W)
        self.efWord = Pmw.EntryField (vFen, validate=Commun.nonVideValidator)
        self.efWord.component('entry').configure(justify="center")
        self.efWord.grid (row = vLigne, column=3 ,sticky=W)
        self.efPlace = Pmw.EntryField (vFen, validate=Commun.nonVideValidator)
        self.efPlace.grid (row = vLigne, column=4 ,sticky=W)
        self.efTime = Commun.heureWidget (vFen, vFen)
        self.efTime.grid (row = vLigne, column=5 ,sticky=W)
        self.efDate = Commun.dateWidget (vFen, vFen)
        self.efDate.grid (row = vLigne, column=6 ,sticky=W)
        vLigne += 1
        Label (vFen, text = "Message Body", fg = "blue", bg = "cyan").grid(row = vLigne, column = 0, columnspan = 7, sticky = W+E)
        vLigne += 1
        Label (vFen, text="TO : ").grid(row=vLigne, column=0, sticky=W)
        self.efDestAction = Pmw.EntryField (vFen, validate=Commun.nonVideValidator)
        self.efDestAction.grid (row=vLigne, column=1, columnspan=2, sticky=E+W)
        vLigne += 1
        Label (vFen, text="TEXT (25 words max.) : ").grid(row=vLigne, column=0, rowspan = 4, sticky=W)
        self.stText = ScrolledText (vFen, wrap="word", height = 3)
        self.stText.grid (row=vLigne, column = 1, columnspan = 7, sticky=E+W)
        vLigne += 4
        Label (vFen, text="FROM : ").grid(row=vLigne, column=0, sticky=W)
        self.efOrigine = Pmw.EntryField (vFen, validate = Commun.nonVideValidator)
        self.efOrigine.grid (row = vLigne, column = 1, columnspan = 2, sticky = W+E)
        vLigne += 1

        Label (vFen,text="Message Footer", fg="blue",bg="cyan").grid(row = vLigne, column = 0, columnspan = 7, sticky = E+W)
        vLigne += 1
        self.fRcv = LabelFrame(vFen, bd = 3)
        self.fRcv.grid(row = vLigne, rowspan = 2, column = 0, columnspan = 3, sticky = N+S)
        Label (self.fRcv, text="RECEIVED FROM").grid(row=vLigne, column=0, sticky=W+E)
        Label (self.fRcv, text="DATE").grid(row=vLigne, column=1, sticky=W+E)
        Label (self.fRcv, text="TIME").grid(row=vLigne, column=2, sticky=W+E)
        self.cbRcvFrom = Commun.indicatifWidget(vFen, self.fRcv, self.root)
        self.cbRcvFrom.grid (row = vLigne+1, column = 0, sticky=W)
        self.efRcvDate = Commun.dateWidget(vFen, self.fRcv)
        self.efRcvDate.component('entry').config(width=10)
        self.efRcvDate.grid (row = vLigne+1, column = 1)
        self.efRcvTime = Commun.heureWidget(vFen, self.fRcv)
        self.efRcvTime.component('entry').config(width=8)
        self.efRcvTime.grid (row = vLigne+1, column = 2)
        self.lAction = StringVar()
        Label (vFen, textvariable = self.lAction).grid(row = vLigne, column=3)
        self.lQrz = StringVar()
        Label (vFen, textvariable = self.lQrz).grid(row = vLigne+1, column=3)
        self.fSen = LabelFrame(vFen, bd = 3)
        self.fSen.grid(row = vLigne, rowspan = 2, column = 4, columnspan = 3, sticky = N+S)
        Label (self.fSen, text="SEND TO").grid(row=vLigne, column = 0, sticky=W+E)
        Label (self.fSen, text="DATE").grid(row=vLigne, column = 1, sticky=W+E)
        Label (self.fSen, text="TIME").grid(row=vLigne, column = 2, sticky=W+E)
        self.cbSenTo = Commun.indicatifWidget(vFen, self.fSen, self.root)
        self.cbSenTo.grid (row=vLigne+1, column = 0, sticky=W)
        self.efSenDate = Commun.dateWidget(vFen, self.fSen)
        self.efSenDate.component('entry').config(width=10)
        self.efSenDate.grid (row = vLigne+1, column = 1)
        self.efSenTime = Commun.heureWidget(vFen, self.fSen)
        self.efSenTime.component('entry').config(width=8)
        self.efSenTime.grid (row = vLigne+1, column = 2)
        vLigne += 2
        Label (vFen,text="Fin de Message ", fg="blue",bg="orange").grid(row=vLigne, column=0, columnspan=8, sticky=E+W)
        vLigne += 1

        Button (vFen, text="Valider", command = self.validerIARU, fg="red", underline = 0).grid(row=vLigne, column=1, padx=5, pady=5, sticky = W+E)
        Button (vFen, text="Annuler", command = self.annulerIARU, fg="red", underline = 1).grid(row=vLigne, column=3, padx=5, pady=5, sticky = W+E)
        Button (vFen, text="Quitter", command = self.quitterIARU, fg="red", underline = 0).grid(row=vLigne, column=5, padx=5, pady=5, sticky = W+E)


    # D�finition des bulles d'aide sur la fen�tre
    def bulleAide(self):
        # ATTENTION, les message d'aide des Widgets GesADRA sont d�j� g�r�s
        self.fenetre.bulle.bind(self.stText, "Texte du message, 25 mots maximum")


    # Action sur un bouton "Valider"
    def validerIARU(self, evt = None):
        "Traitement du bouton 'Valider'"

        #Contr�le de la validit� des donn�es
        if self.controleSaisie() == False:
            # Si erreur, on stoppe le traitement
            return None

        # Cr�ation des fichiers message IARU
        self.redigerIARU()
        
        # Impression
        if self.root.userData['IMPR_MSG'] == "OUI" :
            os.startfile(Commun.getFullPath(self.root, self.vFicIARU+".TXT"), "print")
        else :
            tkMessageBox.showinfo('IARU Message', 'Message cr�� : ' + self.vFicIARU)

        self.fenetre.destroy()

        
    # Action sur le bouton "Annuler"
    def annulerIARU(self, evt = None):
        "Traitement du bouton 'Annuler'"
        # Remise � Z�ro de la saisie
        self.razSaisie()
        # Affichage des boutons
        self.btReceive.grid()
        self.btSend.grid()
        self.btQSP.grid()


    # Action sur le bouton "Quitter"
    def quitterIARU(self, evt = None):
        "Traitement du bouton 'Quitter'"
        etesVousSur = tkMessageBox.askquestion("Fermeture du Formulaire", \
                                               "Confirmez-vous la fermeture du Message IARU ?")
        if etesVousSur == "yes" :
            self.fenetre.destroy()
        else:
            self.fenetre.focus_set()


    # Action sur le bouton "Receiving"
    def rcvIARU(self, evt = None):
        "Traitement du bouton 'Receiving'"
        # Remise � Z�ro de la saisie
        self.razSaisie()
        # Mise en forme de l'affichage
        self.fSen.grid_remove()
        self.fRcv.grid()
        # Initialisation des champs
        self.cAction = "R"
        self.lAction.set("TO")
        self.lQrz.set(self.root.userData['INDICATIF'])
        self.efRcvDate.setvalue(self.vGdh.strftime("%d %b"))
        self.efRcvTime.setvalue(self.vGdh.strftime("%H%M"))
        self.efNumber.component('entry').focus_set()
        # Suppression des boutons
        self.btSend.grid_remove()
        self.btQSP.grid_remove()
        

    # Action sur le bouton "Sending"
    def senIARU(self, evt = None):
        "Traitement du bouton 'Sending'"
        # Remise � Z�ro de la saisie
        self.razSaisie()
        #Mise en forme de l'affichage
        self.fSen.grid()
        self.fRcv.grid_remove()
        # Initialisation des champs
        self.cAction = "S"
        self.efNumber.setvalue(Commun.getNextNumIARU(self.root))
        self.efNumber.component('entry').configure(state = DISABLED)
        self.efStation.setvalue(self.root.userData['INDICATIF'])
        self.efWord.setvalue("Calculated")
        self.efPlace.setvalue(self.root.userData['LOCALITE'])
        self.lAction.set("FROM")
        self.lQrz.set(self.root.userData['INDICATIF'])
        self.efTime.setvalue(self.vGdh.strftime("%H%M"))
        self.efDate.setvalue(self.vGdh.strftime("%d %b"))
        self.efSenDate.setvalue(self.vGdh.strftime("%d %b"))
        self.efSenTime.setvalue(self.vGdh.strftime("%H%M"))
        self.efDestAction.component('entry').focus_set()
        # Suppression des boutons
        self.btReceive.grid_remove()
        self.btQSP.grid_remove()

    # Action sur le bouton "QSP Sending"
    def qspIARU(self, evt = None):
        "Traitement du bouton 'QSP Sending'"
        # Remise � Z�ro de la saisie
        self.razSaisie()
        # Mise en forme de l'affichage
        self.fSen.grid()
        self.fRcv.grid()
        # Initialsation des champs
        self.cAction = "P"
        self.lAction.set("QSP via")
        self.lQrz.set(self.root.userData['INDICATIF'])
        self.efRcvDate.setvalue(self.vGdh.strftime("%d %b"))
        self.efRcvTime.setvalue(self.vGdh.strftime("%H%M"))
        self.efSenDate.setvalue(self.vGdh.strftime("%d %b"))
        self.efSenTime.setvalue(self.vGdh.strftime("%H%M"))
        self.efNumber.component('entry').focus_set()
        # Suppression des boutons
        self.btReceive.grid_remove()
        self.btSend.grid_remove()

    # Traitement du bind <Return> sp�cifique
    def noAction (self, evt = None):
        """Aucune action pour la touche <Entr�e> sur un ScrolledText"""
        return "break"
        

    # Traitement du bind <Tab> sp�cifique
    def nextCtrl (self, evt = None):
        """Restituer l'action de la touche <Tab> sur un ScrolledText"""
        self.efDestAction.component('entry').focus_set()
        return "break"
        

    # Traitement du bind <Focusout> sp�cifique
    def countWords (self, evt = None):
        """Comptage du nombre de mots du ScrolledText"""
        wordList = self.stText.get(1.0,END)
        nbWord = len(wordList.split())
        if nbWord > 25 :
            tkMessageBox.showinfo("Comptage IARU", "Le message contient plus de 25 mots.")
            self.stText.focus_set()
        else :
            if self.cAction == "S" :
                self.efWord.setvalue(str(nbWord).zfill(2))
            else :
                if self.efWord.getvalue() != str(nbWord).zfill(2) :
                    bonCompte = tkMessageBox.askquestion("Comptage IARU", \
                                                        "Le nombre de mots du message (" + str(len(wordList.split())) +\
                                                        ") est diff�rent du compteur.\n"+"Voulez-vous le mettre � jour ?")
                else :
                    bonCompte = "yes"                                        
                if bonCompte == "yes" : self.efWord.setvalue(str(len(wordList.split())).zfill(2))

        self.fenetre.focus_set()
        

    # Remise � z�ro de la saisie utilisateur
    def razSaisie(self):
        self.vGdh = datetime.datetime.now()
        self.cAction = ""
        self.efNumber.component('entry').configure(state = NORMAL)
        self.efNumber.setvalue("")
        self.cbDegUrg.selectitem('Routine')
        self.efStation.setvalue("")
        self.efWord.setvalue("")
        self.efPlace.setvalue("")
        self.efTime.setvalue("")
        self.efDate.setvalue("")
        self.efDestAction.setvalue("")
        self.stText.delete(1.0,END)
        self.efOrigine.setvalue("")
        self.fRcv.grid()
        self.cbRcvFrom.setentry("")
        self.efRcvDate.setvalue("")
        self.efRcvTime.setvalue("")
        self.lAction.set("")
        self.lQrz.set("")
        self.fSen.grid()
        self.cbSenTo.setentry("")
        self.efSenDate.setvalue("")
        self.efSenTime.setvalue("")        
        

    # Validation de la saisie utilisateur
    def controleSaisie(self):
        #Contr�le de saisie
        if not (self.efNumber.valid() and self.efStation.valid() and self.efWord.valid() and \
                self.efPlace.valid() and self.efTime.valid()and self.efDate.valid()):
            tkMessageBox.showwarning('Contr�le', 'Les champs en rouge sont absents ou incorrects')
            self.fenetre.focus_set()
            return False
            
        if not (self.efDestAction.valid() and self.efOrigine.valid()):
            tkMessageBox.showwarning('Contr�le', 'Les champs en rouge sont absents ou incorrects')
            self.fenetre.focus_set()
            return False
            
        self.countWords(self)
        if self.stText.get(1.0, END).strip() == "":
            tkMessageBox.showwarning('Controle', 'Message vide')
            self.stText.focus_set()
            return False

        if self.cAction != "S" and \
           not (self.cbRcvFrom.valid() and self.efRcvDate.valid() and self.efRcvTime.valid()):
            tkMessageBox.showwarning('Contr�le', 'Les champs en rouge sont absents ou incorrects')
            self.fenetre.focus_set()
            return False
       
        if self.cAction != "R" and \
           not (self.cbSenTo.valid() and self.efSenDate.valid() and self.efSenTime.valid()):
            tkMessageBox.showwarning('Contr�le', 'Les champs en rouge sont absents ou incorrects')
            self.fenetre.focus_set()
            return False
       
        return True

        
    # Creation des fichiers message
    def redigerIARU(self):

        # Nom du fichier
        self.vFicIARU = "IARU-" + self.efStation.getvalue() + "-" + self.efNumber.getvalue().zfill(4)
        # Fichier TXT
        self.txtFileIARU()
        # Fichier XML
        self.xmlFileIARU()
        # Fichier MSG (fichier TXT court ne contenant que les donn�es)
        self.msgFileIARU() 
        
        # Ecriture d'une ligne dans la main courante
        vTexte = "Message " + self.vFicIARU + \
		         " de " + self.efOrigine.getvalue() + " vers " +  self.efDestAction.getvalue()
        if self.cAction == "R":
            infosMCI = Commun.InfosMCI(self.vGdh.strftime("%d/%m/%y %H:%M"), self.cbRcvFrom.get(), \
                                   self.lQrz.get(), self.lQrz.get(), " ", vTexte)
        elif self.cAction == "S":
            infosMCI = Commun.InfosMCI(self.vGdh.strftime("%d/%m/%y %H:%M"), self.lQrz.get(), \
                                   self.cbSenTo.get(), self.cbDegUrg.get(), " ", vTexte)
        elif self.cAction == "P":
            infosMCI = Commun.InfosMCI(self.vGdh.strftime("%d/%m/%y %H:%M"), self.cbRcvFrom.get(), \
                                   self.cbSenTo.get(), self.cbDegUrg.get(), " ", vTexte)
        infosMCI.ecrire(self.root)

        # S'il s'agit d'un message �mis : incr�menter le compteur IARU
        if self.cAction == "S": Commun.increaseNumIARU(self.root)


    def txtFileIARU(self):

        fic = open(Commun.getFullPath(self.root, self.vFicIARU+".TXT"),'w')

        fic.write(self.vFicIARU+"\n\n")
        fic.write('################################################################################\n')
        fic.write('- ' +(self.root.userData['ACTIVATION'] + ' - ')*3+'\n')
        fic.write('--------------------------------------------------------------------------------\n')

        # Informations transmission
        if self.cAction == "R":
            fic.write("Emis par     : " + self.cbRcvFrom.get()+"\n")
            fic.write("Recu par     : " + self.lQrz.get()+"\n")
            fic.write("Instructions : " + "Dernier op�rateur " + self.lQrz.get()+"\n")
        elif self.cAction == "S":
            fic.write("Emis par     : " + self.lQrz.get()+"\n")
            fic.write("Recu par     : " + self.cbSenTo.get()+"\n")
            fic.write("Instructions : " + "Premier op�rateur " + self.lQrz.get()+"\n")
        elif self.cAction == "P":
            fic.write("Emis par     : " + self.cbRcvFrom.get()+"\n")
            fic.write("Recu par     : " + self.cbSenTo.get()+"\n")
            fic.write("Instructions : " + "Retransmission par " + self.lQrz.get()+"\n")
        fic.write('================================================================================\n')

        # Ent�te du message
        fic.write("MESSAGE IARU".center(80) + "\n")
        fic.write("Origine      : " + self.efOrigine.getvalue()+"\n")
        fic.write("Dest. Action : " + self.efDestAction.getvalue()+"\n")
        fic.write("Urgence      : " + self.cbDegUrg.get()+"\n")
        fic.write('--------------------------------------------------------------------------------\n')

        # Corps du message
        fic.write("Objet        : " + "Message de " + self.efWord.getvalue() + " mots" +\
                                      " du " + self.efDate.getvalue() +\
                                      " � " + self.efTime.getvalue() +"\n")
        fic.write("R�f�rence    : " + self.efStation.getvalue() + " - " +\
                                      self.efNumber.getvalue()+"\n")
        fic.write("Message : \n\n")
        fic.write(self.stText.get(1.0,END)+"\n")
        fic.write('--------------------------------------------------------------------------------\n')

        # Final du message
        fic.write("GDH R�cept�  : " + self.efRcvDate.getvalue() + " " +\
                                      self.efRcvTime.getvalue() +"\n")
        fic.write("GDH Emission : " + self.efSenDate.getvalue() + " " +\
                                      self.efSenTime.getvalue() +"\n")
        fic.write("FIN DE MESSAGE".center(80) + "\n")
        fic.write('================================================================================\n')
        fic.write('- ' +(self.root.userData['ACTIVATION'] + ' - ')*3+'\n')
        fic.write('################################################################################\n')

        fic.close()

    #
    def xmlFileIARU(self):

        fic = open(Commun.getFullPath(self.root, self.vFicIARU+".XML"),'w')
        #fic.write(self.vFicIARU+"\n\n")
        
        fic.write('<?xml version="1.0" encoding="ISO-8859-15"?><?xml-stylesheet type="text/xsl" href="..\msgIARU.XSL"?>\n')
        fic.write('<message>\n')
        fic.write('<form>IARU Standard Message</form>\n')
        fic.write('<software>' + self.root.userData['LOGICIEL'] + '</software>\n')
        fic.write('<version>' + self.root.userData['VERSION'] + '</version>\n')
        fic.write('<exercise>' + self.root.userData['ACTIVATION'] + '</exercise>\n')
        fic.write('<id>' + self.efNumber.getvalue() + '</id>\n')
        fic.write('<precedance>' + self.cbDegUrg.get() + '</precedance>\n')
        fic.write('<check>'+ self.efWord.getvalue() + '</check>\n')
        fic.write('<filed>')
        fic.write('<date>' + self.efDate.getvalue() + '</date>')
        fic.write('<time>' + self.efTime.getvalue() + '</time>')
        fic.write('</filed>\n')
        fic.write('<origin>')
        fic.write('<station>' + self.efStation.getvalue() + '</station>')
        fic.write('<place>' + self.efPlace.getvalue() + '</place>')
        fic.write('</origin>\n')
        fic.write('<from>' + self.efOrigine.getvalue() + '</from>\n')
        fic.write('<to>' + self.efDestAction.getvalue() + '</to>\n')
        fic.write('<body>')
        fic.write('<para>' + self.stText.get(1.0,END) + '</para>')
        fic.write('</body>\n')
        # Informations transmission
        if self.cAction == "R":
            fic.write('<sentto>')
            fic.write('<name>' + self.lQrz.get() + '</name>')
            fic.write('<date>' + self.efSenDate.getvalue() + '</date>')
            fic.write('<time>' + self.efSenTime.getvalue() + '</time>')
            fic.write('</sentto>\n')
            fic.write('<receivedfrom>')
            fic.write('<name>' + self.cbRcvFrom.get() + '</name>')
            fic.write('<date>' + self.efRcvDate.getvalue() + '</date>')
            fic.write('<time>' + self.efRcvTime.getvalue() + '</time>')
            fic.write('</receivedfrom>\n')
        elif self.cAction == "S":
            fic.write('<sentto>')
            fic.write('<name>' + self.cbSenTo.get() + '</name>')
            fic.write('<date>' + self.efSenDate.getvalue() + '</date>')
            fic.write('<time>' + self.efSenTime.getvalue() + '</time>')
            fic.write('</sentto>\n')
            fic.write('<receivedfrom>')
            fic.write('<name>' + self.lQrz.get() + '</name>')
            fic.write('<date>' + self.efRcvDate.getvalue() + '</date>')
            fic.write('<time>' + self.efRcvTime.getvalue() + '</time>')
            fic.write('</receivedfrom>\n')
        elif self.cAction == "P":
            fic.write('<sentto>')
            fic.write('<name>' + self.cbSenTo.get() + '</name>')
            fic.write('<date>' + self.efSenDate.getvalue() + '</date>')
            fic.write('<time>' + self.efSenTime.getvalue() + '</time>')
            fic.write('</sentto>\n')
            fic.write('<receivedfrom>')
            fic.write('<name>' + self.cbRcvFrom.get() + '</name>')
            fic.write('<date>' + self.efRcvDate.getvalue() + '</date>')
            fic.write('<time>' + self.efRcvTime.getvalue() + '</time>')
            fic.write('</receivedfrom>\n')
            
        fic.write('</message>\n')
    
        fic.close()

    
    # Creation nouveau MSG IARU ###################################################
    def msgFileIARU(self):

        fic = open(Commun.getFullPath(self.root, self.vFicIARU+".MSG"),'w')

        # Corps du message
        fic.write(self.efNumber.get() + " ")
        fic.write(self.cbDegUrg.get() + " ")
        fic.write(self.efStation.getvalue() + " ")
        fic.write(self.efWord.getvalue() + " ")
        fic.write(self.efPlace.getvalue() + " ")
        fic.write(self.efTime.getvalue() + " ")
        fic.write(self.efDate.getvalue() + "\n")
        fic.write("To " + self.efDestAction.getvalue() + "\n")
        fic.write(self.stText.get(1.0,END))
        fic.write("From " + self.efOrigine.getvalue() + "\n")

        fic.close()

