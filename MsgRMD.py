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


###################### Creation d'un message RMD
class FormRMD:
    "Classe d�finissant le formulaire RMD"
    
    def __init__(self, appli):
        "Constructeur de la fen�tre RMD"

        self.root = appli # R�f�rence � l'application racine

        # Cr�ation de la nouvelle fen�tre
        self.fenetre = Commun.nouvelleFenetre(self.root, "Message de Renseignements sur Mati�re Dangereuse")
        # Fermeture par la case syst�me
        self.fenetre.protocol("WM_DELETE_WINDOW", self.quitterMD)

        # Composants de la fen�tre
        self.dessineRMD()

        # Initialisations
        self.razSaisie()
        
        # Gestion des raccourcis clavier
        self.fenetre.bind('<Alt-v>', self.validerMD)
        self.fenetre.bind('<Return>', self.validerMD)
        self.fenetre.bind('<Alt-n>', self.annulerMD)
        self.fenetre.bind('<Escape>', self.annulerMD)
        self.fenetre.bind('<Alt-q>', self.quitterMD)
        self.stComment.bind('<Return>', self.notReturn) # On ne valide pas par <Entr�e> sur la zone stComment
        
    def dessineRMD(self):

        # variables locales
        vLigne = 1 # N� de ligne pour le positionnement des composants
        vFen = self.fenetre

        # Composants de la fen�tre
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
        Label (vFen, text = "Re�u par : ").grid(row = vLigne, column = 3, sticky = W)
        self.cbDestinataire = Commun.indicatifWidget(vFen, vFen, self.root)
        self.cbDestinataire.grid (row = vLigne, column = 4, sticky = W+E)
        vLigne += 1

        Label (vFen, text = "Instructions particuli�res : ").grid(row = vLigne, column = 0, sticky = W)
        self.eInstruc = Entry (vFen)
        self.eInstruc.grid (row = vLigne, column = 1, columnspan = 4, sticky = W+E)
        vLigne += 1

        Label (vFen, text = "Message Mati�res Dangereuses", fg = "blue",bg = "orange").grid(row = vLigne, column = 0, columnspan = 8, sticky = W+E)
        vLigne += 1

        Label (vFen,text = "Ent�te du message", fg = "blue",bg = "cyan").grid(row = vLigne, column = 0,columnspan = 8, sticky = W+E)
        vLigne += 1

        Label (vFen, text = "Origine : ").grid(row = vLigne, column = 0, sticky = W )
        self.efOrigine = Pmw.EntryField (vFen, validate = Commun.nonVideValidator)
        self.efOrigine.grid (row = vLigne, column = 1, sticky = W)
        vLigne += 1

        Label (vFen, text = "Destinataires Action: ").grid(row = vLigne, column = 0, sticky = W)
        self.efDestAction = Pmw.EntryField (vFen, validate = Commun.nonVideValidator)
        self.efDestAction.grid (row = vLigne, column = 1, columnspan = 3, sticky = W+E)
        Label (vFen, text = "(utilisez le / comme s�parateur)").grid(row = vLigne, rowspan = 2, column = 4, columnspan = 3, sticky = W)
        vLigne += 1

        Label (vFen, text = "Destinataires Info: ").grid(row = vLigne, column = 0, sticky = W)
        self.eDestInfo = Entry(vFen)
        self.eDestInfo.grid (row = vLigne, column = 1, columnspan = 3, sticky = W+E)
        vLigne += 1

        Label (vFen, text = "Degr� d'Urgence : ").grid(row = vLigne, column = 0, sticky = W )
        self.cbDegUrg = Commun.comboWidget (self.root, vFen, self.root.cfgListe['DegUrgOBNT'])
        self.cbDegUrg.grid (row = vLigne, column = 1, columnspan = 2, sticky = W)
        vLigne += 1

        Label (vFen,text = "Corps du message", fg = "blue",bg = "cyan").grid( row = vLigne, column = 0,columnspan = 8, sticky = E+W )
        vLigne += 1
        
        # Code Danger
        Label (vFen, text = "Plaque DANGER : " ).grid(row = vLigne, column = 0, rowspan = 2, sticky = W)
        self.fPlaque = LabelFrame(vFen, bd = 0)
        self.fPlaque.grid(row = vLigne, column = 1, rowspan = 2, sticky = W)
        Label (self.fPlaque, text = "Code Danger : " ).grid(row = 0, column = 0, sticky = W)
        Label (self.fPlaque, text = "Numero ONU : " ).grid(row = 1, column = 0, sticky = W)
        self.fDanger = LabelFrame(self.fPlaque, bd = 3, relief='flat', bg='black')
        self.fDanger.grid(row = 0, column = 1, rowspan = 2, sticky = W)
        self.efDanger = Pmw.EntryField (self.fDanger)
        self.efDanger.component('entry').config(justify=CENTER, fg='black', bg='orange', width=8)
        self.efDanger.component('entry').bind('<Key>', Commun.uppercaseKey)
        self.efDanger.component('hull').configure(borderwidth=2, bg='orange')
        self.efDanger.configure(validate = {"validator" : Commun.dangerValidator, "max" : 4, "minstrict" : False, "maxstrict" : False})
        self.efDanger.grid(row = 0, column = 0, sticky = W)
        self.efNumOnu = Pmw.EntryField (self.fDanger)
        self.efNumOnu.component('entry').config(justify=CENTER, fg='black', bg='orange', width=8)
        self.efNumOnu.component('hull').configure(borderwidth=2, bg='orange')
        self.efNumOnu.configure(validate = {"validator" : Commun.onuValidator, "max" : 4, "minstrict" : False, "maxstrict" : False})
        self.efNumOnu.grid(row = 1, column = 0, sticky = W)
        vLigne += 2
        Label (vFen, text = "Pictogramme LOSANGE : " ).grid(row = vLigne, column = 0, sticky = W)
        self.fPicto = LabelFrame(vFen, bd = 0)
        self.fPicto.grid(row = vLigne, column = 1, sticky = W)
        Label (self.fPicto, text = "(code panneau) " ).grid(row = 0, column = 0, sticky = W)
        self.cbPanneau = Commun.comboWidget(vFen, self.fPicto, self.root.cfgListe['CodePicto'], 'orange')
        self.cbPanneau.component('entryfield_entry').config(justify=CENTER, width=6)
        self.cbPanneau.grid(row = 0, column = 1, sticky = W)
        vLigne += 1
        Label (vFen, text = "Etat de la mati�re : " ).grid(row = vLigne, column = 0,sticky = W)
        self.cbEtatMatiere = Commun.comboWidget(vFen, vFen, self.root.cfgListe['EtatMatiere'])
        self.cbEtatMatiere.grid(row = vLigne, column = 1, sticky = W)
        Label (vFen, text = "Si 'AUTRE' pr�cier : " ).grid( row = vLigne, column = 3,sticky = W)
        self.eAutre = Entry (vFen)
        self.eAutre.grid (row = vLigne,column = 4,sticky = W )
        vLigne += 1
        
        Label (vFen, text = "Couleur : " ).grid( row = vLigne, column = 0,sticky = W)
        self.eCouleur = Entry (vFen)
        self.eCouleur.grid ( row = vLigne,column = 1,sticky = W )
        Label (vFen, text = "Odeur : " ).grid( row = vLigne, column = 3,sticky = W)
        self.eOdeur = Entry (vFen)
        self.eOdeur.grid ( row = vLigne,column = 4,sticky = W )
        vLigne += 1

        Label (vFen, text = "Commentaire(s) : ").grid(row = vLigne, column = 0, sticky = W)
        self.stComment = ScrolledText (vFen, wrap = "word", height = 5, width = 80)
        self.stComment.grid (row = vLigne, column = 1, columnspan = 5)
        vLigne += 10

        Label (vFen,text = "Final du message ", fg = "blue",bg = "cyan").grid(row = vLigne, column = 0, columnspan = 6, sticky = E+W)
        vLigne += 1
        Label (vFen, text = "GDH D�p�t/R�daction : ").grid(row = vLigne, column = 0, sticky = W )
        self.efGdhDep = Commun.gdhWidget(vFen, vFen)
        self.efGdhDep.grid (row = vLigne, column = 1, sticky = W)
        self.rbACK = Pmw.RadioSelect(vFen, buttontype = "radiobutton",labelpos = W,label_text = "Demande Accus� de R�ception : ")
        self.rbACK.grid(row = vLigne, column = 3, columnspan = 2, sticky = W)
        self.rbACK.add("Oui")
        self.rbACK.add("Non")
        vLigne += 1
        
        Label (vFen,text = "Fin de message", fg = "blue",bg = "orange").grid( row = vLigne, column = 0,columnspan = 8, sticky = E+W )
        vLigne += 1
        Button (vFen, text = "Valider", command = self.validerMD, fg = "red", underline = 0).grid(row = vLigne, column = 1, padx = 5, pady = 5, sticky = W)
        Button (vFen, text = "Annuler", command = self.annulerMD, fg = "red", underline = 1).grid(row = vLigne, column = 3, padx = 5, pady = 5, sticky = W)
        Button (vFen, text = "Quitter", command = self.quitterMD, fg = "red", underline = 0).grid(row = vLigne, column = 5, padx = 5, pady = 5, sticky = W)


    def validerMD(self, evt = None):
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
        self.redigerRMD()

        # Impression
        if self.root.userData['IMPR_MSG'] == "OUI" :
            os.startfile(Commun.getFullPath(self.root, self.vFicRMD+".TXT"), "print")
        else :
            tkMessageBox.showinfo('Message RMD', 'Message cr�� : ' + self.vFicRMD)
        
	# self.fenetre.destroy


    def annulerMD(self, evt = None):
        self.razSaisie()
        

    def quitterMD(self, evt = None):
        "Traitement du bouton 'Quitter'"
        etesVousSur = tkMessageBox.askquestion("Fermeture du Formulaire", \
                                               "Confirmez-vous la fermeture du Message RMD ?")
        if etesVousSur == "yes" :
            self.fenetre.destroy()
        else:
            self.fenetre.focus_set()
    

    # Traitement du bind <Return> sp�cifique
    def notReturn (self, evt = None):
        """Reproduire le comportement normal de la touche <Entr�e> pour un ScrolledText"""
        self.stComment.insert(self.stComment.index(INSERT), "\n")
        return "break"
    
        
    def razSaisie(self):
        vGdh = datetime.datetime.now().strftime("%d/%m/%y %H:%M")
        self.efGdh.setvalue(vGdh) # Gdh transmission
        self.ckGdh.select() # Cocher pour recalculer le Gdh
        self.cbEmetteur.setentry("")
        self.cbDestinataire.setentry("")
        self.cbDegUrg.selectitem(self.root.userData['URG_RMD'])
        self.eInstruc.delete(0,END)
        self.efOrigine.setvalue("")
        self.efDestAction.setvalue("")
        self.eDestInfo.delete(0, END)
        self.efDanger.setvalue("")
        self.efNumOnu.setvalue("")
        self.cbPanneau.selectitem(0)
        self.cbEtatMatiere.selectitem(0)
        self.eAutre.delete(0,END)
        self.eCouleur.delete(0,END)
        self.eOdeur.delete(0,END)
        self.stComment.delete(1.0,END)
        self.efGdhDep.setvalue(vGdh) # Gdh r�daction message
        self.rbACK.invoke("Non") # Demande Ack

        
    def controleSaisie(self):
        if not (self.efGdh.valid() and self.cbEmetteur.valid() and self.cbDestinataire.valid() and \
                self.efOrigine.valid() and self.efDestAction.valid()):
            tkMessageBox.showwarning('Contr�le', 'Les champs en rouge sont absents ou incorrects')
            self.fenetre.focus_set()
            return False
        
        return True 


    # Cr�ation des fichiers message
    def redigerRMD(self):

        # Nom du fichier
        self.vFicRMD = Commun.getFicRMD(self.root)
        # Fichier TXT
        self.txtFileRMD()
        # Fichier XML
        self.xmlFileRMD()
        
        # Ecriture d'une ligne dans la main courante
        vTexte = "Message " + self.vFicRMD + \
		         " de " + self.efOrigine.getvalue() + " vers " +  self.efDestAction.getvalue()
        infosMCI = Commun.InfosMCI(self.efGdh.getvalue(), self.cbEmetteur.get(), self.cbDestinataire.get(), \
                                   self.cbDegUrg.get(), " ", vTexte)
        infosMCI.ecrire(self.root)
        
    
    def txtFileRMD(self):
        
        fic = open(Commun.getFullPath(self.root, self.vFicRMD+".TXT"),'w')
        
        fic.write(self.vFicRMD+"\n\n")
        fic.write('################################################################################\n')
        fic.write('- ' +(self.root.userData['ACTIVATION'] + ' - ')*3+'\n')
        fic.write('--------------------------------------------------------------------------------\n')

        # Informations transmission
        fic.write("GDH Emission : " + self.efGdh.getvalue()+ "\n")
        fic.write("Emis par     : " + self.cbEmetteur.get()+ "\n")
        fic.write("Re�u par     : " + self.cbDestinataire.get()+ "\n")
        fic.write("Instructions : " + self.eInstruc.get()+ "\n")
        fic.write('================================================================================\n')

        # Ent�te du message
        fic.write("MESSAGE RENSEIGNEMENT MATIERE DANGEUREUSE".center(80) + "\n")
        fic.write("Origine      : " + self.efOrigine.getvalue()+"\n")
        fic.write("Dest. Action : " + self.efDestAction.getvalue()+"\n")
        fic.write("Dest. Info   : " + self.eDestInfo.get()+"\n")
        fic.write("Urgence      : " + self.cbDegUrg.get()+"\n")
        fic.write('--------------------------------------------------------------------------------\n')

        # Corps du message
        fic.write("Plaque DANGER \n")
        fic.write("Code Danger  : " + self.efDanger.getvalue()+"\n")
        fic.write("Numero ONU   : " + self.efNumOnu.getvalue()+"\n")
        fic.write("Picto. LOSANGE \n")
        fic.write("Code Panneau : " + self.cbPanneau.get()+"\n")
        fic.write("\n")
        fic.write("Etat mati�re : " + self.cbEtatMatiere.get()+"\n")
        fic.write("Si 'AUTRE'   : " + self.eAutre.get()+"\n")
        fic.write("Couleur      : " + self.eCouleur.get()+"\n")
        fic.write("Odeur        : " + self.eOdeur.get()+"\n")
        fic.write("Commentaire  : \n\n")
        # d�coupage des lignes du commentaire
        for ligne in self.stComment.get(1.0,END).split("\n"):
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
    def xmlFileRMD(self):

        fic = open(Commun.getFullPath(self.root, self.vFicRMD+".XML"),'w')
        
        fic.write('<?xml version="1.0" encoding="iso-8859-15"?><?xml-stylesheet type="text/xsl" href="..\msgRMD.XSL"?>\n')
        fic.write('<msg>\n')
        fic.write('<form>Message RMD</form>\n')
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
        fic.write("<danger>" + self.efDanger.getvalue()+"</danger>\n")
        fic.write("<numonu>" + self.efNumOnu.getvalue()+"</numonu>\n")
        fic.write("<panno>" + self.cbPanneau.get()+"</panno>\n")
        fic.write("<matiere>" + self.cbEtatMatiere.get()+"</matiere>\n")
        fic.write("<autre>" + self.eAutre.get()+"</autre>\n")
        fic.write("<couleur>" + self.eCouleur.get()+"</couleur>\n")
        fic.write("<odeur>" + self.eOdeur.get()+"</odeur>\n")
        # d�coupage des lignes du commentaire
        for ligne in self.stComment.get(1.0,END).split("\n"):
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