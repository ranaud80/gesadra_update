# -*- coding: iso-8859-15 -*-

from tkinter import *

import datetime
import time
import os
import Pmw
import re

### FONCTIONS COMMUNES ############################
#
#   Classées par famille : 
#       - Gestion des fichiers
#       - Objets graphiques élaborés (widgets)
#       - Validateurs
#       - Autres fonctions
#       - Classes
#
### FONCTIONS COMMUNES ############################

def getNextNumIARU(root):
    """Rendre le numéro du message IARU suivant"""
    vInd = int(root.userData['NUM_IARU'])
    vNum = str(vInd+1).zfill(4)
    return vNum
#
#
def increaseNumIARU(root):
    """Incrémenter le numéro de message IARU"""
    root.userData['NUM_IARU'] = getNextNumIARU(root)
#
#    
### FICHIERS ######################################
#
def getSession(root):
    """Rendre le répertoire de la session"""
    try:
        vRep = root.userData['SESSION']
    except KeyError:
        vRep = "S"+datetime.datetime.now().strftime("%Y%m%d")
        root.userData['SESSION'] = vRep
        
    return vRep
#
#
def getFicSession(root):
    """Rendre le nom du fichier de la session"""
    return getSession(root)+".ini"
#
#
def getFicReseau(root):
    """Rendre le nom du fichier du réseau"""
    return getSession(root)+".net"
#
#
def getRepertoire(root):
    """Rendre le répertoire d'exploitation"""
    try:
        vRep = root.userData['REPTRAVAIL']
    except KeyError:
        vRep = os.getcwd()
        
    return vRep
#
#
def getFullPath(root, fichier):
    """ rendre le path complet du fichier à traiter"""
    vFic = os.path.join(getRepertoire(root), fichier)
    return vFic
#
#
def getFicMCI(root):
    """Rendre le nom du fichier Main Courante"""
    try:
        vFic = root.userData['FIC_MCI']
    except KeyError:        
        vFic = root.userData['INDICATIF'].upper()
        vFic = 'MCI-' + vFic + '.CSV'
    return vFic
#
#
def getFicGSat(root):
    """Rendre le nom du fichier des releves SATER"""
    try:
        vFic = root.userData['FIC_SATER']
    except KeyError:        
        vFic = root.userData['INDICATIF'].upper()
        vFic = 'SAT-' + vFic + '.CSV'
    return vFic
#
#
def getFicGVict(root):
    """Rendre le nom du fichier des victimes"""
    try:
        vFic = root.userData['FIC_VICT']
    except KeyError:        
        vFic = root.userData['INDICATIF'].upper()
        vFic = 'VIC-' + vFic + '.CSV'
    return vFic
#
#
def getFicGPoi(root):
    """Rendre le nom du fichier des points particuliers"""
    try:
        vFic = root.userData['FIC_CARTO']
    except KeyError:        
        vFic = root.userData['INDICATIF'].upper()
        vFic = 'POI-' + vFic + '.CSV'
    return vFic
#
#
def getFicREZO(root):
    """Rendre le nom du fichier RESEAU"""
    vInd = int(root.userData['NUM_REZO'])
    vNum = str(vInd+1).zfill(4)
    root.userData['NUM_REZO'] = vNum
    
    return "RESEAU-" + vNum
#
#
def getFicOBNT(root):
    """Rendre le nom du fichier message OBNT"""
    vInd = int(root.userData['NUM_OBNT'])
    vNum = str(vInd+1).zfill(4)
    root.userData['NUM_OBNT'] = vNum
    vFic = root.userData['INDICATIF'].upper()
    
    return "OBNT-" + vFic + "-" + vNum
#
#
def getFicSATER(root):
    """Rendre le nom du fichier message OBNT"""
    vInd = int(root.userData['NUM_SATER'])
    vNum = str(vInd+1).zfill(4)
    root.userData['NUM_SATER'] = vNum
    vFic = root.userData['INDICATIF'].upper()
    
    return "SATER-" + vFic + "-" + vNum
#
#
def getFicPOI(root):
    """Rendre le nom du fichier message OBNT"""
    vInd = int(root.userData['NUM_POI'])
    vNum = str(vInd+1).zfill(4)
    root.userData['NUM_POI'] = vNum
    vFic = root.userData['INDICATIF'].upper()
    
    return "POI-" + vFic + "-" + vNum
#
#
def getFicBT(root):
    """Rendre le nom du fichier message BT"""
    vInd = int(root.userData['NUM_BT'])
    vNum = str(vInd+1).zfill(4)
    root.userData['NUM_BT'] = vNum
    vFic = root.userData['INDICATIF'].upper()
    
    return "BILTMP-" + vFic + "-" + vNum
#
#
def getFicDM(root):
    """Rendre le nom du fichier message DM"""
    vInd = int(root.userData['NUM_DM'])
    vNum = str(vInd+1).zfill(4)
    root.userData['NUM_DM'] = vNum
    vFic = root.userData['INDICATIF'].upper()
    
    return "DM-" + vFic + "-" + vNum
#
#
def getFicTMD(root):
    """Rendre le nom du fichier message TMD"""
    vInd = int(root.userData['NUM_TMD'])
    vNum = str(vInd+1).zfill(4)
    root.userData['NUM_TMD'] = vNum
    vFic = root.userData['INDICATIF'].upper()
    
    return "TMD-" + vFic + "-" + vNum
#
#
def getFicRMD(root):
    """Rendre le nom du fichier message RMD"""
    vInd = int(root.userData['NUM_RMD'])
    vNum = str(vInd+1).zfill(4)
    root.userData['NUM_RMD'] = vNum
    vFic = root.userData['INDICATIF'].upper()
    
    return "RMD-" + vFic + "-" + vNum
#
#
def getFicBilAmb(root):
    """Rendre le nom du fichier Bilan Ambiance"""
    vInd = int(root.userData['NUM_BILAMB'])
    vNum = str(vInd+1).zfill(4)
    root.userData['NUM_BILAMB'] = vNum
    vFic = root.userData['INDICATIF'].upper()
    
    return "BILAMB-" + vFic + "-" + vNum
#
#
def getFicBILSEC(root):
    """Rendre le nom du fichier Bilan Secouriste"""
    vInd = int(root.userData['NUM_BILSEC'])
    vNum = str(vInd+1).zfill(4)
    root.userData['NUM_BILSEC'] = vNum
    vFic = root.userData['INDICATIF'].upper()
    
    return "BILSEC-" + vFic + "-" + vNum
#
#
def getNumVict(root):
    """Rendre le numéro de victime"""
    vInd = int(root.userData['NUM_VICT'])
    vNum = str(vInd+1).zfill(5)
    root.userData['NUM_VICT'] = vNum
    
    return vNum
#
#
# WIDGETS #
#
def nouvelleFenetre(root, titre):
    """Créer une nouvelle fenetre Toplevel"""

    # Nouvelle fenêtre pour Pmw
    fenetre = Toplevel(root)
    Pmw.initialise(fenetre)

    # Paramétrage de la fenêtre
    fenetre.resizable(width = False, height = False)
    fenetre.wm_state()
    if ( sys.platform.startswith('win')): 
        fenetre.iconbitmap("appli.ico")
    fenetre.title (titre +" - Activation : " + root.userData['ACTIVATION'])

    # Instanciation d'une bulle d'aide
    fenetre.bulle = Pmw.Balloon(fenetre, relmouse = 'both')

    # Focus
    fenetre.focus_set()

    return fenetre
#
#
def gdhWidget(fenetre, frame):
    """Créer un champ GDH avec ses contraites et vérifications"""
    ctrl = Pmw.EntryField (frame)
    ctrl.configure(validate = {"validator" : gdhValidator, "min" : 14, "max" : 14, "minstrict" : False, "maxstrict" : False})
    fenetre.bulle.bind(ctrl, "Date (jj/mm/aa) <espace> Heure (hh:mm)")

    return ctrl
#
#
def dateWidget(fenetre, frame):
    """Créer un champ date avec ses contraites et vérifications"""
    ctrl = Pmw.EntryField (frame)
    ctrl.configure(validate = {"validator" : dateValidator, "min" : 6, "max" : 6, "minstrict" : False, "maxstrict" : False})
    fenetre.bulle.bind(ctrl, "Date (jj mmm)")

    return ctrl
#
#
def heureWidget(fenetre, frame):
    """Créer un champ heure avec ses contraites et vérifications"""
    ctrl = Pmw.EntryField (frame)
    ctrl.configure(validate = {"validator" : timeValidator, "min" : 4, "max" : 4, "minstrict" : False, "maxstrict" : False})
    fenetre.bulle.bind(ctrl, "Heure (hhmm)")

    return ctrl
#
#
def indicatifWidget(fenetre, frame, root):
    """Créer et alimenter une combobox de type indicatif avec ses contraites et vérifications"""
    ctrl = Pmw.ComboBox (frame, scrolledlist_items = getListeReseau(root), listheight = 80)
    ctrl.configure(entryfield_validate = {"validator" : indicatifValidator, "min" : 2, "max" : 8, "minstrict" : False, "maxstrict" : False})
    ctrl.component('entry').bind('<Key>', uppercaseKey)
    fenetre.bulle.bind(ctrl, "Indicatif de 2 à 8 car., sans espace (tiret, slash et souligné permis)")

    return ctrl
#
#
def comboWidget (fenetre, frame, liste, bg='white', taille = 80):
    """Créer et alimenter une combobox sans saisie, sans en modifier l'aspect"""
    ctrl = Pmw.ComboBox(frame, scrolledlist_items = liste, listheight = taille, history = 0)
    ctrl.component('entryfield_entry').configure(state = DISABLED, disabledforeground = 'black', disabledbackground = bg)
    fenetre.bulle.bind(ctrl, "Sélection sans saisie")

    return ctrl
#
#
def coordWidget (fenetre, frame):
    """Créer un entry-field de saisie de coordonnées"""
    ctrl = Pmw.EntryField (frame, validate = {"max" : 12, "maxstrict" : False, "validator" : nonVideValidator})
    fenetre.bulle.bind(ctrl, "Coordonnée jusqu'à 12 car., sans contrôle de saisie")
    
    return ctrl
   
#
#
# VALIDATEURS #
#
def nonVideValidator(text):
    """Validateur champ non vide"""
    if text.strip() == "":
        return Pmw.PARTIAL
    else:
        return Pmw.OK
#
#                              
def gdhValidator(text):
    """Validateur des champs GDH"""
    try:
        time.strptime(text, "%d/%m/%y %H:%M")
    except:
        return Pmw.PARTIAL
    else:
        return Pmw.OK
#                             
#                                            
def dateValidator(text):
    """Validateur des champs date IARU"""
    try:
        time.strptime(text, "%d %b")
    except:
        return Pmw.PARTIAL
    else:
        return Pmw.OK
#                              
#                              
def timeValidator(text):
    """Validateur des champs heure IARU"""
    try:
        time.strptime(text, "%H%M")
    except:
        return Pmw.PARTIAL
    else:
        return Pmw.OK
#                              
#                              
_indicatif = re.compile ('^[A-Za-z][-/_A-Za-z0-9]*$')
def indicatifValidator(text):
    """Validateur des champs obligatoires de type indicatif"""
    if _indicatif.match(text) is None :
        return Pmw.PARTIAL
    else :
        return Pmw.OK
#        
#                              
def tacticValidator(text):
    """Validateur des champs optionnels de type indicatif"""
    # Le champ peut être vide
    if text.strip() == '': return Pmw.OK
    # S'il est renseigné, longueur mini : deux caractères
    if len(text) < 2 : return Pmw.PARTIAL
    # Contrôle des caractères
    if _indicatif.match(text) is None :
        return Pmw.PARTIAL
    else :
        return Pmw.OK
#                             
#                              
def indicatif3Validator(text):
    """Validateur du champ indicatif saisi depuis la Main Courante"""
    # Contrôle de la longueur
    if len(text) < 2 or len(text) > 8 : return Pmw.PARTIAL
    # Contrôle des caractères
    if _indicatif.match(text) is None :
        return Pmw.PARTIAL
    else:
        return Pmw.OK
#        
#                              
_session = re.compile ('^[A-Za-z][-_A-Za-z0-9]*$')
def sessionValidator(text):
    """Validateur des champs obligatoires de type session"""
    if _session.match(text) is None :
        return Pmw.PARTIAL
    else :
        return Pmw.OK
#        
#                              
_danger = re.compile ('^X?[0-9]{2,3}$')
def dangerValidator(text):
    """Validateur des champs obligatoires de type code danger"""
    if _danger.match(text) is None :
        return Pmw.PARTIAL
    else :
        return Pmw.OK
#                              
#        
_numOnu = re.compile ('^[0-9]{1,4}$')
def onuValidator(text):
    """Validateur des champs obligatoires de type code danger"""
    if _numOnu.match(text) is None :
        return Pmw.PARTIAL
    else :
        return Pmw.OK
#                              
#                              
_numVict = re.compile ('^[0-9]{1,5}$')
def numValidator(text):
    """Validateur des champs obligatoires de type numéro"""
    # Le champ peut être vide
    if text.strip() == 'Auto': return Pmw.OK
    # S'il est renseigné, il est numérique
    if _numVict.match(text) is None :
        return Pmw.PARTIAL
    else :
        return Pmw.OK
#
#
# AUTRES FONCTIONS #
#
def encode (chaine):
    try:
        return chaine.encode ('iso-8859-15')
    except:
        print (chaine)
        return "?"
#
def getListeReseau(root):
    """Constituer la liste des stations du réseau"""
    liste = []
    liste.append(root.userData["INDICATIF"])
    for i in range(1,15):
        if root.netData["STATION"+str(i)] != "" : liste.append(root.netData["STATION"+str(i)])
    return liste
#
def uppercaseKey(event):
    """Modifier le caractère saisi par sa majuscule"""
    if (event.char == event.keysym) and (event.char != event.char.upper()):
        event.widget.event_generate(event.char.upper())
        return "break"
#
#
# CLASSES #
#
class InfosRezo:
    "Classe définissant une ligne d'infos du Réseau"

    def __init__(self, indicatif, tactic, operateur, statut, local, coordX, coordY, comment):
        "Constructeur de l'objet InfosQRZ"
        self._Indicatif = indicatif
        self._Tactic    = tactic
        self._Operateur = operateur
        self._Statut    = statut
        self._Localis   = local
        self._PosX      = coordX
        self._PosY      = coordY
        self._Comment   = comment
        
    # Methode privée pour création de l'entête du fichier
    def _entete (self, fichier):
        fic = open (fichier,'a')
        fic.write ("Indicatif;Alias Tactic;Operateurs;Statut;Localisation;Coord_X;Coord_Y;Commentaire\n")
        fic.close()

    # Ecriture de la ligne dans le fichier
    def ecrire (self, root):

        vFic = getFullPath(root, getFicRezo(root))
        if not os.path.isfile(vFic): self._entete(vFic)
                               
        vLigne = self._Indicatif +";"+\
                 self._Tactic    +";"+\
                 self._Operateur +";"+\
                 self._Statut    +";"+\
                 self._Localis   +";"+\
                 self._PosX      +";"+\
                 self._PosY      +";"+\
                 self._Comment   +"\n"

        fic = open (vFic,'a')
        fic.write(vLigne)
        fic.close()
        
		# Mise à jour de la main courante (si ouverte)
        # if root.fenReseau != None: root.fenMCI.afficherListe(self)

        # Impression d'une Trace
        # if root.userData['TRACE'] == "OUI": self.tracer(root)


    # Rendu pour affichage à l'écran
    def getLigne (self, root):

        # mise en forme pour l'affichage
        vLigne = self._Indicatif.ljust(8)+"  "+\
                 self._Tactic.ljust(12)+"  "+\
                 self._Operateur.ljust(20)+"  "+\
                 self._Statut.ljust(12)+"  "+\
                 self._Local.ljust(20)+"  "+\
                 self._CoordX.ljust(12)+"  "+\
                 self._CoordY.ljust(12)+"  "+\
                 self._Comment.ljust(30)

        return vLigne

    # Rendre le statut
    def getStatut(self):
        return self._Statut
#
#
class InfosMCI:
    "Classe définissant une ligne d'infos de la Main Courante"

    def __init__(self, gdh, emetteur, destinataire, urgence, moyen, texte):
        "Constructeur de l'objet InfosMCI"
        self._Gdh = gdh
        vGdh = gdh.split (" ")
        self._Date = vGdh[0]
        self._Heure = vGdh[1]
        self._Emetteur = emetteur
        self._Destinataire = destinataire
        self._Urg = urgence
        self._MoyTrans = moyen
        self._Texte = texte

    # Methode privée pour création de l'entête du fichier
    def _entete (self, fichier):
        fic = open (fichier,'a')
        fic.write ("GDH;MoyTrans;Emetteur;Destinataire;DegUrg;Texte\n")
#        CREATE TABLE "Log-Mci" ("GDH" TEXT NOT NULL , "MoyTrans" TEXT NOT NULL , "Emetteur" TEXT NOT NULL , "Destinataire" TEXT NOT NULL , "DegUrg" TEXT NOT NULL , "Texte" TEXT NOT NULL )
        fic.close()

    # Ecriture de la ligne dans le fichier
    def ecrire (self, root):

        vFic = getFullPath(root, getFicMCI(root))
        if not os.path.isfile(vFic): self._entete(vFic)
                               
        vLigne = self._Gdh+";"+\
                 self._MoyTrans+";"+\
                 self._Emetteur+";"+\
                 self._Destinataire+";"+\
                 self._Urg+";"+\
                 self._Texte+"\n"

        fic = open (vFic,'a')
        fic.write(vLigne)
        fic.close()
        
		# Mise à jour de la main courante (si ouverte)
        if root.fenMCI != None: root.fenMCI.afficherListe(self)

        # Impression d'une Trace
        if root.userData['TRACE'] == "OUI": self.tracer(root)


    # Rendu pour affichage à l'écran
    def getLigne (self, root):

        # mise en forme pour l'affichage
        vLigne = " " + \
                 self._Heure.ljust(5)+" | "+\
                 self._Emetteur.ljust(10)+" | "+\
                 self._Destinataire.ljust(10)+" | "+\
                 self._Urg.ljust(17)+" | "+\
                 self._Texte

        return vLigne

    # Rendre le degré d'urgence
    def getUrg(self):
        return self._Urg    

    def tracer(self, root):

        vAlerte = root.userData['ACTIVATION']

        fic = open(getFullPath(root, "TRACE.TXT"),'w')
        fic.write('################################################################################\n')
        fic.write('- ' + (vAlerte + ' - ')*3 + '\n')
        fic.write("================================================================================\n")
        fic.write(("INFORMATION MAIN COURANTE DU RESEAU " + root.userData['SERVICE']).center(80) + "\n")
        fic.write("--------------------------------------------------------------------------------\n")
        fic.write("Service      : " + encode (root.userData['SERVICE']) + "\n")
        fic.write("Emetteur     : " + encode (self._Emetteur) + "\n")
        fic.write("Destinataire : " + encode (self._Destinataire) + "\n")
        fic.write("--------------------------------------------------------------------------------\n")
        fic.write("Date         : " + encode (self._Date) + "\n")
        fic.write("Heure        : " + encode (self._Heure) + "\n")
        fic.write("Transmis en  : " + encode (self._MoyTrans) + "\n")
        fic.write("--------------------------------------------------------------------------------\n")
        fic.write("Information  : \n")
        fic.write(encode (self._Texte) + "\n")
        fic.write("FIN D'INFORMATION".center(80) + "\n")
        fic.write("================================================================================\n")
        fic.write('- ' +(vAlerte + ' - ')*3+'\n')
        fic.write('################################################################################\n')
        fic.close()

        os.startfile(getFullPath(root, "TRACE.TXT"), "print")
#
#
class InfosSATER:
    """Classe définissant une ligne d'infos de la Gestion SATER"""
    
    def __init__(self, gdh, emetteur, destinataire, systeme, datum, coordX, coordY, direction, force, commentaire):
        """Constructeur de l'objet InfosSATER"""
        self._Gdh = gdh
        vGdh = gdh.split (" ")
        self._Date = vGdh[0]
        self._Heure = vGdh[1]
        self._Emetteur = emetteur
        self._Destinataire = destinataire
        self._Systeme = systeme
        self._Datum = datum
        self._CoordX = coordX
        self._CoordY = coordY
        self._Dir = direction
        self._Force = force
        self._Comment = commentaire

    # Methode privée pour création de l'entête du fichier
    def _entete (self, fichier):
        fic = open (fichier,'a')
        fic.write ("GDH;Emetteur;Destinataire;Systeme;Datum;CoordX;CoordY;Dir;Force;Comment\n")
#       CREATE TABLE "Log-Sater" ("GDH"  NOT NULL , "Emetteur"  NOT NULL , "Destinataire"  NOT NULL , "Systeme"  NOT NULL , "Datum"  NOT NULL , "CoordX"  NOT NULL , "CoordY"  NOT NULL , "Direction"  NOT NULL , "Force"  NOT NULL , "Comment" )
        fic.close()

    # Ecriture de la ligne dans le fichier
    def ecrire (self, root):

        vFic = getFullPath(root, getFicGSat(root))
        if not os.path.isfile (vFic): self._entete(vFic)
                               
        vLigne = self._Gdh+";"+\
                 self._Emetteur+";"+\
                 self._Destinataire+";"+\
                 self._Systeme+";"+\
                 self._Datum+";"+\
                 self._CoordX+";"+\
                 self._CoordY+";"+\
                 self._Dir+";"+\
                 self._Force+";"+\
                 self._Comment+"\n"

        fic = open (vFic,'a')
        fic.write(vLigne)
        fic.close()


    # Rendu pour affichage à l'écran
    def getLigne (self, root):

        # mise en forme pour l'affichage
        vLigne = " " + \
                 self._Heure.ljust(5)+" | "+\
                 self._Emetteur.ljust(10)+" | "+\
                 self._CoordX.ljust(12)+" | "+\
                 self._CoordY.ljust(12)+" | "+\
                 self._Dir.ljust(5)+" | "+\
                 self._Force.ljust(5)+" | "+\
                 self._Comment 

        return vLigne
#
#
class InfosPOI:
    """Classe définissant une ligne d'infos de la Gestion POI"""
    
    def __init__(self, gdh, emetteur, destinataire, systeme, datum, coordX, coordY, typReleve, detail, commentaire):
        """Constructeur de l'objet InfosPOI"""
        self._Gdh = gdh
        vGdh = gdh.split (" ")
        self._Date = vGdh[0]
        self._Heure = vGdh[1]
        self._Emetteur = emetteur
        self._Destinataire = destinataire
        self._Systeme = systeme
        self._Datum = datum
        self._CoordX = coordX
        self._CoordY = coordY
        self._Type = typReleve
        self._Detail = detail
        self._Comment = commentaire

    # Methode privée pour création de l'entête du fichier
    def _entete (self, fichier):
        fic = open (fichier,'a')
        fic.write ("GDH;Emetteur;Destinataire;Systeme;Datum;CoordX;CoordY;Type;Detail;Comment\n")
#       CREATE TABLE "Log-Carto" ("GDH" TEXT NOT NULL , "Emetteur" TEXT NOT NULL , "Destinataire" TEXT NOT NULL , "Systeme" TEXT NOT NULL , "Datum" TEXT NOT NULL , "CoordX" TEXT NOT NULL , "CoordY" TEXT NOT NULL , "Type" TEXT NOT NULL , "Detail" TEXT NOT NULL , "Comment" TEXT)        
        fic.close()

    # Ecriture de la ligne dans le fichier
    def ecrire (self, root):

        vFic = getFullPath(root, getFicGPoi(root))
        if not os.path.isfile (vFic): self._entete(vFic)
                               
        vLigne = self._Gdh+";"+\
                 self._Emetteur+";"+\
                 self._Destinataire+";"+\
                 self._Systeme+";"+\
                 self._Datum+";"+\
                 self._CoordX+";"+\
                 self._CoordY+";"+\
                 self._Type+";"+\
                 self._Detail+";"+\
                 self._Comment+"\n"

        fic = open (vFic,'a')
        fic.write(vLigne)
        fic.close()


    # Rendu pour affichage à l'écran
    def getLigne (self, root):

        # mise en forme pour l'affichage
        vLigne = " " + \
                 self._Heure.ljust(5)+" | "+\
                 self._Emetteur.ljust(10)+" | "+\
                 self._CoordX.ljust(12)+" | "+\
                 self._CoordY.ljust(12)+" | "+\
                 self._Type.ljust(16)+" | "+\
                 self._Detail.ljust(25)+" | "+\
                 self._Comment

        return vLigne
#
#
class InfosVict:
    """Classe définissant une ligne d'infos de la Gestion des victimes"""
    
    def __init__(self, gdh, num, age, sexe, nom, nature, vitale, urgence, autre):
        """Constructeur de l'objet InfosVict"""
        self._Gdh = gdh
        vGdh = gdh.split (" ")
        self._Date = vGdh[0]
        self._Heure = vGdh[1]
        self._Num = num
        self._Age = age
        self._Sexe = sexe
        self._Nom = nom
        self._Nature = nature
        self._Vitale = vitale
        self._Urgence = urgence
        self._Autre = autre

    # Methode privée pour création de l'entête du fichier
    def _entete (self, fichier):
        fic = open (fichier,'a')
        fic.write ("GDH;Numero;Age;Sexe;Nom;Nature;Vitale;Urgence;Autre\n")
        fic.close()

    # Ecriture de la ligne dans le fichier
    def ecrire (self, root):

        vFic = getFullPath(root, getFicGVict(root))
        if not os.path.isfile (vFic): self._entete(vFic)
                               
        vLigne = self._Gdh+";"+\
                 self._Num +";"+\
                 self._Age +";"+\
                 self._Sexe +";"+\
                 self._Nom +";"+\
                 self._Nature +";"+\
                 self._Vitale +";"+\
                 self._Urgence +";"+\
                 self._Autre+"\n"

        fic = open (vFic,'a')
        fic.write(vLigne)
        fic.close()

    # Rendu pour affichage à l'écran
    def getLigne (self, root):

        # mise en forme pour l'affichage
        vLigne = " " + \
                 self._Heure.ljust(5)+" | "+\
                 self._Num.ljust(6)+" | "+\
                 self._Age.ljust(10)+" | "+\
                 self._Sexe.ljust(3)+" | "+\
                 self._Nom.ljust(16)+" | "+\
                 self._Nature.ljust(12)+" | "+\
                 self._Vitale.ljust(12)+" | "+\
                 self._Urgence.ljust(12)+" | "+\
                 self._Autre.ljust(30)

        return vLigne
#
#