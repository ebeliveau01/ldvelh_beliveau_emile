/*
 * Creation des tables de la base de données
*/

DROP DATABASE IF EXISTS ldvelh_beliveau_emile;
CREATE DATABASE ldvelh_beliveau_emile;

USE ldvelh_beliveau_emile;

#DROP TABLE IF EXISTS livre;
CREATE TABLE livre (
    id integer primary key auto_increment,
    titre varchar(255)
);

#DROP TABLE IF EXISTS chapitre;
CREATE TABLE chapitre (
    id integer primary key auto_increment,
    no_chapitre varchar(255),
    texte text,
    id_livre integer,

    foreign key (id_livre) references livre(id)
);

#DROP TABLE IF EXISTS lien_chapitre;
CREATE TABLE lien_chapitre (
    id integer primary key auto_increment,
    no_chapitre_origine integer,
    no_chapitre_destination integer,

    foreign key (no_chapitre_origine) references chapitre(id),
    foreign key (no_chapitre_destination) references chapitre(id)
);

#DROP TABLE IF EXISTS personnage;
CREATE TABLE personnage (
    id integer primary key auto_increment,
    nom_perso varchar(255),
    bourse integer DEFAULT 0,
    points_habilete integer DEFAULT 0,
    endurance integer DEFAULT 0,
    objets_speciaux text DEFAULT "",
    repas text DEFAULT "",
    objets text DEFAULT ""
);

#DROP TABLE IF EXISTS armes;
CREATE TABLE armes (
    id integer primary key auto_increment,
    nom varchar(255)
);

#DROP TABLE IF EXISTS perso_arme;
CREATE TABLE perso_armes (
    id integer primary key auto_increment,
    id_perso integer,
    id_arme integer DEFAULT 1,
    no_arme integer,

    foreign key (id_perso) references personnage(id),
    foreign key (id_arme) references armes(id)
);

#DROP TABLE IF EXISTS discipline;
CREATE TABLE discipline (
    id integer primary key auto_increment,
    nom varchar(255)
);

#DROP TABLE IF EXISTS perso_discipline;
CREATE TABLE perso_discipline (
    id integer primary key auto_increment,
    id_perso integer,
    id_discipline integer DEFAULT 1,
    no_discipline integer,

    foreign key (id_perso) references personnage(id),
    foreign key (id_discipline) references discipline(id)
);

CREATE TABLE sauvegarde (
	id integer primary key auto_increment,
	id_livre integer,
	id_chapitre_dernier integer,
	id_perso integer,
	
	foreign key (id_livre) references livre(id),
	foreign key (id_chapitre_dernier) references chapitre(id),
	foreign key (id_perso) references personnage(id)
);

/*
 * Insertion des diciplines et des armes
 */

/* Livre */
INSERT INTO livre (titre) VALUES ("Les maîtres des ténèbres");

/* Dicipline */
INSERT INTO discipline (nom) VALUES 
	("Vide"),
    ("Le camouflage"),
    ("La chasse"),
    ("Le sixième sens"),
    ("L'oriantarion"),
    ("La guérison"),
    ("La maîtrise des armes"),
    ("Bouclier psychique"),
    ("Puissance psychique"),
    ("Communication animale"),
    ("Maître psychique de la matière");

/* Arme */
INSERT INTO armes (nom) VALUES
	("Vide"),
    ("Poignard"),
    ("Lance"),
    ("Masse d'armes"),
    ("Sabre"),
    ("Marteau de guerre"),
    ("Épée gauche"),
    ("Hache"),
    ("Épée droite"),
    ("Baton"),
    ("Glaive");

/*
 * Création de l'utilisateur pour le jeu
 * Ainsi que l'attribution des droits sur la table du jeu
 */
CREATE USER IF NOT EXISTS 'joueur'@'%' IDENTIFIED BY '8888';

GRANT SELECT, INSERT, UPDATE, DELETE ON ldvelh_beliveau_emile.* TO 'joueur';