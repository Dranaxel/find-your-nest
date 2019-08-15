#!/usr/bin/env python3

from flask import Flask, request, redirect, render_template, session
import sqlite3

conn = sqlite3.connect('findyournest.db', check_same_thread=False)
c = conn.cursor()

# TABLE adresses
c.execute("""
    CREATE TABLE IF NOT EXISTS adresse (
        id_adresse INTEGER PRIMARY KEY AUTOINCREMENT,
        nb INTEGER,
        rue VARCHAR(255),
        code_postal INTEGER,
        ville VARCHAR(255)
    )
    """)

c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (1, 'chemin Scribe', 92190, 'Meudon')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (1, 'villa Adrien', 92190,'Meudon')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (100, 'boulevard Raspail', 75006, 'Paris')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (15, 'rue de Sèvres', 75006, 'Paris')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (25, 'rue de Vaugirard', 75006, 'Paris')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (16, 'rue Linné', 75005, 'Paris')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (17, 'rue des Grands Augustins', 75006, 'Paris')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (13, 'rue du Dr Arnaudet', 92190, 'Meudon')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (27, 'avenue du Bas Meudon', 92190, 'Meudon')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (55, 'rue Abbé Cartin', 75014, 'Paris')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (21, 'rue du Clos', 75020, 'Paris')""")        
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (70, 'rue Irénée Blanc', 75020, 'Paris')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (19, 'rue de Paul Strauss', 75020, 'Paris')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (147, 'rue Belliard', 75018, 'Paris')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (1, 'Sentier des Brillants', 92190, 'Meudon')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (14, 'rue Tolain', 75020, 'Paris')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (8, 'rue des Mercades', 92190, 'Meudon')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (82, 'avenue du Général Leclerc', 75014, 'Paris')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (11, 'avenue du Général Juin', 92360, 'Meudon')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (6, 'rue Rougemont', 75009, 'Paris')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (2, 'cour Saint-Emilion', 75012, 'Paris')""")


#TABLE DES UTILISATEURS 
c.execute("""
    CREATE TABLE IF NOT EXISTS utilisateur (
        id_utilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
        prenom VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        password VARCHAR(15) NOT NULL,
        budget INTEGER, 
        temps TIME, 
        id_adresse INTEGER,
        type_logement VARCHAR(50),
        FOREIGN KEY (id_adresse) REFERENCES adresse (id_adresse),
        FOREIGN KEY (type_logement) REFERENCES logement(type_logement)
    )
    """)

c.execute("""INSERT INTO utilisateur (prenom, email, password, budget, temps, id_adresse, type_logement) VALUES ('Lola', 'lola@gmail.com', 'lolafyn', 2700,'01:00', 19, 'appartement')""")
c.execute("""INSERT INTO utilisateur (prenom, email, password, budget, temps, id_adresse, type_logement) VALUES ('Hocan', 'hocan@gmail.com', 'hocanfyn', 1900, '00:30', 20, 'appartement') """)
c.execute("""INSERT INTO utilisateur (prenom, email, password, budget, temps, id_adresse, type_logement) VALUES ('Sarah', 'sarah@gmail.com', 'sarahfyn', 4000, '00:45', 21, 'maison')""")

# TABLE DES LOGEMENTS
c.execute("""
    CREATE TABLE IF NOT EXISTS logement (
        id_logement INTEGER PRIMARY KEY AUTOINCREMENT,
        type_logement VARCHAR(255),
        nb_piece INTEGER,
        prix INTEGER,
        superficie INTEGER, 
        id_adresse INTEGER,
        FOREIGN KEY (id_adresse) REFERENCES adresse (id_adresse)
    )
    """)

c.execute("""INSERT INTO logement (type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('appartement', 5, 4300, 102, 1)""")
c.execute("""INSERT INTO logement (type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('appartement', 2, 2400, 45, 2)""")
c.execute("""INSERT INTO logement (type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('appartemeent', 4, 3300, 91, 3)""")
c.execute("""INSERT INTO logement (type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('appartement', 4, 4100, 100, 4)""")
c.execute("""INSERT INTO logement (type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('appartement', 5, 3800, 115, 5)""")
c.execute("""INSERT INTO logement (type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('appartement', 5, 4150, 188, 6)""")
c.execute("""INSERT INTO logement (type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('appartement', 2, 2400, 28, 7)""")
c.execute("""INSERT INTO logement (type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('appartement', 2, 2900, 43, 8)""")
c.execute("""INSERT INTO logement (type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('maison', 7, 4080, 150, 9)""")
c.execute("""INSERT INTO logement (type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('maison', 6, 3999, 128, 10)""")
c.execute("""INSERT INTO logement (type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('maison', 7, 4560, 194, 11)""")
c.execute("""INSERT INTO logement (type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('maison', 5, 3980, 102, 12)""")
c.execute("""INSERT INTO logement (type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('maison', 8, 5066, 300, 13)""")
c.execute("""INSERT INTO logement (type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('maison', 6, 3600, 135, 14)""")
c.execute("""INSERT INTO logement (type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('maison', 3, 3200, 100, 15)""")
c.execute("""INSERT INTO logement (type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('appartement', 1, 855, 22, 16)""")
c.execute("""INSERT INTO logement (type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('appartement', 2, 1153, 52, 17)""")
c.execute("""INSERT INTO logement (type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('appartement', 3, 2000, 60, 18)""")


# TABLE favoris 
c.execute("""
    CREATE TABLE IF NOT EXISTS favoris(
    id_favoris INTEGER PRIMARY KEY AUTOINCREMENT, 
    id_utilisateur INTERGER,
    id_logement INTEGER,
    FOREIGN KEY (id_utilisateur) REFERENCES utilisateur (id_utilisateur),
    FOREIGN KEY (id_logement) REFERENCES logement (id_logement)
)
""")

c.execute("""INSERT INTO favoris (id_utilisateur, id_logement) VALUES (1, 17)""")
c.execute("""INSERT INTO favoris (id_utilisateur, id_logement) VALUES (2, 3)""")
c.execute("""INSERT INTO favoris (id_utilisateur, id_logement) VALUES (2,6)""")
c.execute("""INSERT INTO favoris (id_utilisateur, id_logement) VALUES (2,4)""")

conn.commit()
conn.close()


