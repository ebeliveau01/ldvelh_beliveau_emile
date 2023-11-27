import sys
import mysql.connector
from PyQt5.QtWidgets import QApplication, QMainWindow
# Importer la classe Ui_MainWindow du fichier demo.py
from mainWindow import Ui_MainWindow

#Informations de connection à la base de données. Changer les infos dépendament de la bd à laquelle on essait de se connecter.
try:
    mydb = mysql.connector.connect(
        host="localhost",
        user="joueur",
        password="8888",
        database="ldvelh_beliveau_emile"
    )
    print("Connexion réussi")
except ValueError:
    print("Erreur lors de la connexion")

# En paramêtre de la classe MainWindow on va hériter des fonctionnalités
# de QMainWindow et de notre interface Ui_MainWindow
class MainWindow(QMainWindow, Ui_MainWindow):
    id_personnage = None
    id_livre = 1
    id_chapitre = 1
    id_sauvegarde = 0

    def __init__(self, *args, obj=None, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.setupUi(self)

        self.afficher_livre()
        self.afficher_sauvegarde()
        self.chargerDiscipline()
        self.chargerArme()
        self.pushButton_nouvelle_partie.clicked.connect(self.nouvellePartie)
        self.pushButton_chapitre_destination.clicked.connect(self.changer_chapitre)
        self.pushButton_charger_partie.clicked.connect(self.charger)
        self.pushButton_sauvegarder_partie.clicked.connect(self.sauvegarder)
        self.pushButton_supprimer_partie.clicked.connect(self.supprimer)

    #Cette fonction affiche le livre actuel dans lequel on joue.
    def afficher_livre(self):
        mycursor = mydb.cursor()
        mycursor.execute("SELECT titre FROM livre")
        resultat = mycursor.fetchall()
        for (titre_livre) in resultat:
            self.comboBox_livre.addItem(titre_livre[0])

    # Function qui crée un nouveau personnage et qui commence une nouvelle partie
    def nouvellePartie(self):
        if self.lineEdit_nom_personnage.text() == "":
            self.label_nom_personnage.setText("Veuillez choisir un nom.")
        else:
            cursor = mydb.cursor()
            requete = "INSERT INTO personnage(nom_perso) VALUES (%s)"
            valeur = (self.lineEdit_nom_personnage.text(),)
            try:
                cursor.execute(requete,valeur)
                self.id_personnage = cursor.lastrowid
                mydb.commit()
            except mysql.Error as erreur:
                print(erreur)

            self.afficher_chapitre('Avertir le roi')
            self.afficher_choix_chapitre('Avertir le roi')

            self.chargerDiscipline()
            self.chargerArme()
            self.afficherJoueur


            self.lineEdit_nom_personnage.clear()
            self.comboBox_partie_dispo.clear()

            self.id_chapitre = 1
            self.id_sauvegarde = 0

    # Fonction qui affiche le nom du chapitre ouvert
    def afficher_nom_chapitre(self, nomChapitre):
        self.label_nom_chapitre.setText(nomChapitre)

    # Fonction qui affiche le chapitre demandé
    def afficher_chapitre(self, noChapitre):
        self.textBrowser_chapitre.clear

        nomChapitre = "Chapitre: "+noChapitre
        self.afficher_nom_chapitre(nomChapitre)

        mycursor = mydb.cursor()

        requete = ("SELECT texte FROM chapitre WHERE no_chapitre = %s")
        #Il faut mettre une virgule après parce que ce doit être un TUPLE, et non un int.
        valeur = (noChapitre,)

        try:
            mycursor.execute(requete,valeur)
        except ValueError:
            print("Il y a eu une erreur lors de l'exécution de la requête.")

        resultat = mycursor.fetchall()

        if resultat == None:
            print("Une erreur à eu lieu")
            self.textBrowser_chapitre.setText("Une erreur à eu lieu")
        else:
            self.textBrowser_chapitre.setText(resultat[0][0])

    # Fonction qui affiche les possibilitées de chapitre qui sont possible
    def afficher_choix_chapitre(self, noChapitre):
        self.comboBox_chapitre_destination.clear()

        if (noChapitre == 'Avertir le roi'):
            self.comboBox_chapitre_destination.addItem(str(1))
            return
        
        mycursor = mydb.cursor()

        requete = "SELECT no_chapitre_destination FROM lien_chapitre WHERE no_chapitre_origine = %s"
        valeur = (noChapitre,)
        try:
            mycursor.execute(requete,valeur)

        except ValueError:
            print("Une erreur est survenu")

        resultat = mycursor.fetchall()

        for(no_chapitre_destination) in resultat:
            self.comboBox_chapitre_destination.addItem(str(no_chapitre_destination[0]))

    # Fonction qui permet de changer de chapitre
    def changer_chapitre(self):
        choixChapitre = self.comboBox_chapitre_destination.currentText()

        if (choixChapitre != ""):
            self.afficher_chapitre(choixChapitre)
            self.afficher_choix_chapitre(choixChapitre)
            self.id_chapitre = int(choixChapitre)

    # Fonction qui affiche toutes les sauvegardes disponibles
    def afficher_sauvegarde(self):
        self.comboBox_partie_dispo.clear()

        mycursor = mydb.cursor()

        requete = "SELECT sauvegarde.id,nom_perso FROM sauvegarde INNER JOIN personnage ON sauvegarde.id_perso = personnage.id ORDER BY sauvegarde.id"
        try:
            mycursor.execute(requete)
        except ValueError:
            print("Une erreur à eu lieu")
        
        resultat = mycursor.fetchall()
        
        for(nom_personnage) in resultat:
            self.comboBox_partie_dispo.addItem(str(nom_personnage[0])+": "+str(nom_personnage[1]))

    # Function qui sauvegarder la partie actuelle
    def sauvegarder(self):
        cursor = mydb.cursor()

        requete = "SELECT id_livre FROM sauvegarde WHERE id = %s"
        valeur = (self.id_sauvegarde,)

        cursor.execute(requete,valeur)
        resultat = cursor.fetchall()

        if (len(resultat) != 0):
            requete = "UPDATE sauvegarde SET id_chapitre_dernier=%s WHERE id = %s"
            valeur = (self.id_chapitre,self.id_sauvegarde)
            try:
                cursor.execute(requete,valeur)
                mydb.commit()
            except ValueError:
                print("Erreur lors de la sauvegarde")
        else:
            requete = "INSERT INTO sauvegarde(id_livre,id_chapitre_dernier,id_perso) VALUES (%s,%s,%s)"
            valeur = (self.id_livre,self.id_chapitre,self.id_personnage)
            try:
                cursor.execute(requete,valeur)
                self.id_sauvegarde = cursor.lastrowid
                mydb.commit()
            except ValueError:
                print("Erreur lors de la sauvegarde")
        self.afficher_sauvegarde()
        self.sauvegarderDiscipline()
        self.sauvegarderArme()
        self.sauvegarderJoueur()

    # Fonction qui charge une partie déjà enregistrer
    def charger(self):
        choixSauvegarde = self.comboBox_partie_dispo.currentText()
        choix = choixSauvegarde.split(':')

        cursor = mydb.cursor()

        texte = "SELECT id_livre,id_chapitre_dernier,id_perso FROM sauvegarde WHERE id = %s"
        value = (choix[0],)
        try:
            cursor.execute(texte,value)
        except ValueError:
            print("Erreur lors de la requête.")
        resultat = cursor.fetchall()

        self.id_sauvegarde = choix[0]
        self.id_livre = resultat[0][0]
        self.id_chapitre = resultat[0][1]
        self.id_personnage = resultat[0][2]

        self.afficher_chapitre(str(resultat[0][1]))
        self.afficher_choix_chapitre(str(resultat[0][1]))
        self.chargerDiscipline()
        self.chargerArme()
        self.afficherJoueur()

    # Supprimer la partie actuelle.
    def supprimer(self):
        if (self.id_sauvegarde != 0):
            mycursor = mydb.cursor()
            texte = "DELETE FROM sauvegarde WHERE id = %s"
            value = (self.id_sauvegarde,)
            try:
                mycursor.execute(texte,value)
                mydb.commit()
            except ValueError:
                print("Erreur lors de la requête.")

            self.textBrowser_chapitre.clear()

            self.comboBox_discipline_1.clear()
            self.comboBox_discipline_2.clear()
            self.comboBox_discipline_3.clear()
            self.comboBox_discipline_4.clear()
            self.comboBox_discipline_5.clear()
            self.comboBox_discipline_6.clear()

            self.comboBox_arme_1.clear()
            self.comboBox_arme_2.clear()

            self.label_nom_chapitre.clear()

            self.afficher_sauvegarde()

    # Charge les disciplines dans les combos box et sélectionne celle du joueur
    def chargerDiscipline(self):
        cursor = mydb.cursor()

        texte = "SELECT id,nom FROM discipline"
        try:
            cursor.execute(texte)
        except ValueError:
            print("Une erreur est survenu")

        resultat = cursor.fetchall()

        for(nom_discipline) in resultat:
            self.comboBox_discipline_1.addItem(str(nom_discipline[0])+": "+str(nom_discipline[1]))
            self.comboBox_discipline_2.addItem(str(nom_discipline[0])+": "+str(nom_discipline[1]))
            self.comboBox_discipline_3.addItem(str(nom_discipline[0])+": "+str(nom_discipline[1]))
            self.comboBox_discipline_4.addItem(str(nom_discipline[0])+": "+str(nom_discipline[1]))
            self.comboBox_discipline_5.addItem(str(nom_discipline[0])+": "+str(nom_discipline[1]))
            self.comboBox_discipline_6.addItem(str(nom_discipline[0])+": "+str(nom_discipline[1]))
        
        if (self.id_personnage != None):
            texte = "SELECT nom,id_discipline,no_discipline FROM discipline INNER JOIN perso_discipline ON id_discipline = discipline.id WHERE id_perso = %s"
            valeur = (self.id_personnage,)
            try:
                cursor.execute(texte,valeur)
            except ValueError:
                print("Une erreur est survenu")

            resultat = cursor.fetchall()

            for(discipline_joueur) in resultat:
                if (discipline_joueur[2] == 1):
                    self.comboBox_discipline_1.setCurrentText(str(discipline_joueur[1])+": "+str(discipline_joueur[0]))
                elif (discipline_joueur[2] == 2):
                    self.comboBox_discipline_2.setCurrentText(str(discipline_joueur[1])+": "+str(discipline_joueur[0]))
                elif (discipline_joueur[2] == 3):
                    self.comboBox_discipline_3.setCurrentText(str(discipline_joueur[1])+": "+str(discipline_joueur[0]))
                elif (discipline_joueur[2] == 4):
                    self.comboBox_discipline_4.setCurrentText(str(discipline_joueur[1])+": "+str(discipline_joueur[0]))
                elif (discipline_joueur[2] == 5):
                    self.comboBox_discipline_5.setCurrentText(str(discipline_joueur[1])+": "+str(discipline_joueur[0]))
                elif (discipline_joueur[2] == 6):
                    self.comboBox_discipline_6.setCurrentText(str(discipline_joueur[1])+": "+str(discipline_joueur[0]))

    # Update une discipline du joueur selon son numéro de discipline
    def updateDiscipline(self, idDiscipline, noDiscipline):
        cursor = mydb.cursor()

        requete = "UPDATE perso_discipline SET id_discipline=%s WHERE id_perso = %s AND no_discipline = %s"
        valeur = (idDiscipline,self.id_personnage,noDiscipline)
        try:
            cursor.execute(requete,valeur)
            mydb.commit()
        except ValueError:
            print("Erreur lors de la sauvegarde")

    # Sauvegarde toutes les disciplines du joueur
    def sauvegarderDiscipline(self):
        discipline1 = self.comboBox_discipline_1.currentText().split(':')
        discipline2 = self.comboBox_discipline_2.currentText().split(':')
        discipline3 = self.comboBox_discipline_3.currentText().split(':')
        discipline4 = self.comboBox_discipline_4.currentText().split(':')
        discipline5 = self.comboBox_discipline_5.currentText().split(':')
        discipline6 = self.comboBox_discipline_6.currentText().split(':')

        self.updateDiscipline(discipline1[0],1)
        self.updateDiscipline(discipline2[0],2)
        self.updateDiscipline(discipline3[0],3)
        self.updateDiscipline(discipline4[0],4)
        self.updateDiscipline(discipline5[0],5)
        self.updateDiscipline(discipline6[0],6)

    # Charge les armes dans les combos box et sélectionne celle du joueur
    def chargerArme(self):
        cursor = mydb.cursor()

        texte = "SELECT id,nom FROM armes"
        try:
            cursor.execute(texte)
        except ValueError:
            print("Une erreur est survenu")

        resultat = cursor.fetchall()

        for(nom_arme) in resultat:
            self.comboBox_arme_1.addItem(str(nom_arme[0])+": "+str(nom_arme[1]))
            self.comboBox_arme_2.addItem(str(nom_arme[0])+": "+str(nom_arme[1]))
        
        if (self.id_personnage != None):
            texte = "SELECT nom,id_arme,no_arme FROM armes INNER JOIN perso_armes ON id_arme = armes.id WHERE id_perso = %s"
            valeur = (self.id_personnage,)
            try:
                cursor.execute(texte,valeur)
            except ValueError:
                print("Une erreur est survenu")

            resultat = cursor.fetchall()

            for(arme_joueur) in resultat:
                if (arme_joueur[2] == 1):
                    self.comboBox_arme_1.setCurrentText(str(arme_joueur[1])+": "+str(arme_joueur[0]))
                elif (arme_joueur[2] == 2):
                    self.comboBox_arme_2.setCurrentText(str(arme_joueur[1])+": "+str(arme_joueur[0]))

    # Update une arme du joueur selon son numéro d'arme
    def updateArme(self, idArme, noArme):
        cursor = mydb.cursor()

        requete = "UPDATE perso_armes SET id_arme=%s WHERE id_perso = %s AND no_arme = %s"
        valeur = (idArme,self.id_personnage,noArme)
        try:
            cursor.execute(requete,valeur)
            mydb.commit()
        except ValueError:
            print("Erreur lors de la sauvegarde")

    # Sauvegarde toutes les armes du joueur
    def sauvegarderArme(self):
        arme1 = self.comboBox_arme_1.currentText().split(':')
        arme2 = self.comboBox_arme_2.currentText().split(':')

        self.updateArme(arme1[0],1)
        self.updateArme(arme2[0],2)

    # Affiche tous les aspects du joueur autre que les disciplines et les armes
    def afficherJoueur(self):
        cursor = mydb.cursor()

        texte = "SELECT bourse,points_habilete,endurance,objets_speciaux,repas,objets FROM personnage WHERE id = %s"
        valeur = (self.id_personnage,)
        try:
            cursor.execute(texte,valeur)
        except ValueError:
            print("Une erreur est survenu")

        resultat = cursor.fetchall()

        self.textEdit_bourse.clear()
        self.textEdit_points_habilete.clear()
        self.textEdit_endurance.clear()
        self.textEdit_objets_speciaux.clear()
        self.textEdit_repas.clear()
        self.textEdit_objets.clear()

        self.textEdit_bourse.setText(str(resultat[0][0]))
        self.textEdit_points_habilete.setText(str(resultat[0][1]))
        self.textEdit_endurance.setText(str(resultat[0][2]))
        self.textEdit_objets_speciaux.setText(str(resultat[0][3]))
        self.textEdit_repas.setText(str(resultat[0][4]))
        self.textEdit_objets.setText(str(resultat[0][5]))

    # Sauvegarde tous les aspects du joueur autre que les disciplines et les armes
    def sauvegarderJoueur(self):
        cursor = mydb.cursor()

        bourse = self.textEdit_bourse.toPlainText()
        pointsHabilete = self.textEdit_points_habilete.toPlainText()
        endurance = self.textEdit_endurance.toPlainText()
        objetsSpeciaux = self.textEdit_objets_speciaux.toPlainText()
        repas = self.textEdit_repas.toPlainText()
        objets = self.textEdit_objets.toPlainText()

        requete = "UPDATE personnage SET bourse=%s,points_habilete=%s,endurance=%s,objets_speciaux=%s,repas=%s,objets=%s WHERE id = %s"
        valeur = (bourse,pointsHabilete,endurance,objetsSpeciaux,repas,objets,self.id_personnage)

        try:
            cursor.execute(requete,valeur)
            mydb.commit()
        except ValueError:
            print("Erreur lors de la sauvegarde")

app = QApplication(sys.argv)

window = MainWindow()
window.show()
app.exec()