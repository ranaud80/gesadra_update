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


###################### Creation d'un message RMD
class FormRMD:
    "Classe définissant le formulaire RMD"
    
    def __init__(self, appli):
        "Constructeur de la fenêtre RMD"

        self.root = appli # Référence à l'application racine

        # Création de la nouvelle fenêtre
        self.fenetre = Commun.nouvelleFenetre(self.root, "Message de Renseignements sur Matière Dangereuse")
        # Fermeture par la case système
        self.fenetre.protocol("WM_DELETE_WINDOW", self.quitterMD)

        # Composants de la fenêtre
        self.dessineRMD()

        # Initialisations
        self.razSaisie()
        
        # Gestion des raccourcis clavier
        self.fenetre.bind('<Alt-v>', self.validerMD)
        self.fenetre.bind('<Return>', self.validerMD)
        self.fenetre.bind('<Alt-n>', self.annulerMD)
        self.fenetre.bind('<Escape>', self.annulerMD)
        self.fenetre.bind('<Alt-q>', self.quitterMD)
        self.stComment.bind('<Return>', self.notReturn) # On ne valide pas par <Entrée> sur la zone stComment
        
    def dessineRMD(self):

        # variables locales
        vLigne = 1 # N° de ligne pour le positionnement des composants
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
        self.cbDestinataire.grid (row = vLigne, column = 4, sticky = W+E)
        vLigne += 1

        Label (vFen, text = "Instructions particulières : ").grid(row = vLigne, column = 0, sticky = W)
        self.eInstruc = Entry (vFen)
        self.eInstruc.grid (row = vLigne, column = 1, columnspan = 4, sticky = W+E)
        vLigne += 1

        Label (vFen, text = "Message Matières Dangereuses", fg = "blue",bg = "orange").grid(row = vLigne, column = 0, columnspan = 8, sticky = W+E)
        vLigne += 1

        Label (vFen,text = "Entête du message", fg = "blue",bg = "cyan").grid(row = vLigne, column = 0,columnspan = 8, sticky = W+E)
        vLigne += 1

        Label (vFen, text = "Origine : ").grid(row = vLigne, column = 0, sticky = W )
        self.efOrigine = Pmw.EntryField (vFen, validate = Commun.nonVideValidator)
        self.efOrigine.grid (row = vLigne, column = 1, sticky = W)
        vLigne += 1

        Label (vFen, text = "Destinataires Action: ").grid(row = vLigne, column = 0, sticky = W)
        self.efDestAction = Pmw.EntryField (vFen, validate = Commun.nonVideValidator)
        self.efDestAction.grid (row = vLigne, column = 1, columnspan = 3, sticky = W+E)
        Label (vFen, text = "(utilisez le / comme séparateur)").grid(row = vLigne, rowspan = 2, column = 4, columnspan = 3, sticky = W)
        vLigne += 1

        Label (vFen, text = "Destinataires Info: ").grid(row = vLigne, column = 0, sticky = W)
        self.eDestInfo = Entry(vFen)
        self.eDestInfo.grid (row = vLigne, column = 1, columnspan = 3, sticky = W+E)
        vLigne += 1

        Label (vFen, text = "Degré d'Urgence : ").grid(row = vLigne, column = 0, sticky = W )
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
        Label (vFen, text = "Etat de la matière : " ).grid(row = vLigne, column = 0,sticky = W)
        self.cbEtatMatiere = Commun.comboWidget(vFen, vFen, self.root.cfgListe['EtatMatiere'])
        self.cbEtatMatiere.grid(row = vLigne, column = 1, sticky = W)
        Label (vFen, text = "Si 'AUTRE' précier : " ).grid( row = vLigne, column = 3,sticky = W)
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
        Label (vFen, text = "GDH Dépôt/Rédaction : ").grid(row = vLigne, column = 0, sticky = W )
        self.efGdhDep = Commun.gdhWidget(vFen, vFen)
        self.efGdhDep.grid (row = vLigne, column = 1, sticky = W)
        self.rbACK = Pmw.RadioSelect(vFen, buttontype = "radiobutton",labelpos = W,label_text = "Demande Accusé de Réception : ")
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
        self.redigerRMD()

        # Impression
        if self.root.userData['IMPR_MSG'] == "OUI" :
            os.startfile(Commun.getFullPath(self.root, self.vFicRMD+".TXT"), "print")
        else :
            tkMessageBox.showinfo('Message RMD', 'Message créé : ' + self.vFicRMD)
        
	self.fenetre.destroy()


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
    

    # Traitement du bind <Return> spécifique
    def notReturn (self, evt = None):
        """Reproduire le comportement normal de la touche <Entrée> pour un ScrolledText"""
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
        self.efGdhDep.setvalue(vGdh) # Gdh rédaction message
        self.rbACK.invoke("Non") # Demande Ack

        
    def controleSaisie(self):
        if not (self.efGdh.valid() and self.cbEmetteur.valid() and self.cbDestinataire.valid() and \
                self.efOrigine.valid() and self.efDestAction.valid()):
            tkMessageBox.showwarning('Contrôle', 'Les champs en rouge sont absents ou incorrects')
            self.fenetre.focus_set()
            return False
        
        return True 


    # Création des fichiers message
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
        fic.write("GDH Emission : " + Commun.encode (self.efGdh.getvalue())+ "\n")
        fic.write("Emis par     : " + Commun.encode (self.cbEmetteur.get())+ "\n")
        fic.write("Reçu par     : " + Commun.encode (self.cbDestinataire.get())+ "\n")
        fic.write("Instructions : " + Commun.encode (self.eInstruc.get())+ "\n")
        fic.write('================================================================================\n')

        # Entête du message
        fic.write("MESSAGE RENSEIGNEMENT MATIERE DANGEUREUSE".center(80) + "\n")
        fic.write("Origine      : " + Commun.encode (self.efOrigine.getvalue())+"\n")
        fic.write("Dest. Action : " + Commun.encode (self.efDestAction.getvalue())+"\n")
        fic.write("Dest. Info   : " + Commun.encode (self.eDestInfo.get())+"\n")
        fic.write("Urgence      : " + Commun.encode (self.cbDegUrg.get())+"\n")
        fic.write('--------------------------------------------------------------------------------\n')

        # Corps du message
        fic.write("Plaque DANGER \n")
        fic.write("Code Danger  : " + Commun.encode (self.efDanger.getvalue())+"\n")
        fic.write("Numero ONU   : " + Commun.encode (self.efNumOnu.getvalue())+"\n")
        fic.write("Picto. LOSANGE \n")
        fic.write("Code Panneau : " + Commun.encode (self.cbPanneau.get())+"\n")
        fic.write("\n")
        fic.write("Etat matière : " + Commun.encode (self.cbEtatMatiere.get())+"\n")
        fic.write("Si 'AUTRE'   : " + Commun.encode (self.eAutre.get())+"\n")
        fic.write("Couleur      : " + Commun.encode (self.eCouleur.get())+"\n")
        fic.write("Odeur        : " + Commun.encode (self.eOdeur.get())+"\n")
        fic.write("Commentaire  : \n\n")
        # découpage des lignes du commentaire
        for ligne in Commun.encode(self.stComment.get(1.0,END)).split("\n"):
            if len(ligne) > 79:
                for ligne in textwrap.wrap(ligne,79):
                    fic.write(ligne +"\n")
            else:
               fic.write(ligne + "\n")
        fic.write('--------------------------------------------------------------------------------\n')

        # Final du message
        fic.write("GDH Dépôt    : " + Commun.encode (self.efGdhDep.getvalue())+"\n")
        fic.write("Demande A.R. : " + Commun.encode (self.rbACK.getvalue())+"\n")
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
        fic.write("<danger>" + Commun.encode (self.efDanger.getvalue())+"</danger>\n")
        fic.write("<numonu>" + Commun.encode (self.efNumOnu.getvalue())+"</numonu>\n")
        fic.write("<panno>" + Commun.encode (self.cbPanneau.get())+"</panno>\n")
        fic.write("<matiere>" + Commun.encode (self.cbEtatMatiere.get())+"</matiere>\n")
        fic.write("<autre>" + Commun.encode (self.eAutre.get())+"</autre>\n")
        fic.write("<couleur>" + Commun.encode (self.eCouleur.get())+"</couleur>\n")
        fic.write("<odeur>" + Commun.encode (self.eOdeur.get())+"</odeur>\n")
        # découpage des lignes du commentaire
        for ligne in Commun.encode(self.stComment.get(1.0,END)).split("\n"):
            if len(ligne) > 79:
                for ligne in textwrap.wrap(ligne,79):
                    fic.write("<txt>" + ligne +"</txt>\n")
            else:
               fic.write("<txt>" + ligne + "</txt>\n")
        fic.write('</corps>\n')
        fic.write('<bot>\n')
        fic.write("<gdh>" + Commun.encode(self.efGdhDep.getvalue())+"</gdh>\n")
        fic.write("<ack>" + Commun.encode(self.rbACK.getvalue())+"</ack>\n")
        fic.write('</bot>\n')
            
        fic.write('</msg>\n')
    
        fic.close()
    #