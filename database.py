#!/usr/bin/env python3

from flask import Flask, request, redirect, render_template, session
import sqlite3
from passlib.hash import sha256_crypt

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

c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (69, 'rue St Sabin', 75011, 'Paris')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (30, 'rue de Pétion', 75011, 'Paris')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (11, 'rue de Guébriant', 75020, 'Paris')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (5, 'rue des Orfèvres', 75001, 'Paris')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (10, 'rue Vivienne', 75002, 'Paris')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (57, 'rue Castagnary', 75015, 'Paris')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (2, 'rue Charbonnel', 75013, 'Paris')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (48, 'avenue de Saxe', 75007, 'Paris')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (57, 'avenue Philippe-Auguste', 75011, 'Paris')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (11, 'rue Picot', 75116, 'Paris')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (5, 'rue Pierre Mouillard', 75020, 'Paris')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (58, 'rue Leibniz', 75018, 'Paris')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (5, 'rue Lucien et Edouard Gerber', 92240, 'Malakoff')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (32, 'rue Carnot', 92100, 'Boulogne-Billancourt')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (67, 'avenue Henri Barbusse', 92140, 'Clamart' )""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (23, 'avenue de la Belle Gabrielle', 92150, 'Suresnes')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (42, 'rue Martin Levasseur', 93400, 'Saint-Ouen')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (45, 'Chemin Latéral', 94140, 'Maisons-Alfort')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (7, 'rue des Galons', 92190, 'Meudon')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (82, 'avenue du Général Leclerc', 75014, 'Paris')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (11, 'avenue du Général Juin', 92360, 'Meudon')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (6, 'rue Rougemont', 75009, 'Paris')""")
c.execute("""INSERT INTO adresse (nb, rue, code_postal, ville) VALUES (2, 'cour Saint-Emilion', 75012, 'Paris')""")

# TABLE DES LOGEMENTS
c.execute("""
    CREATE TABLE IF NOT EXISTS logement (
        id_logement INTEGER PRIMARY KEY AUTOINCREMENT,
        titre VARCHAR(50),
        photo BLOB, 
        description VARCHAR(500), 
        nb_chambre INTEGER,
        type_logement VARCHAR(255),
        nb_piece INTEGER,
        prix INTEGER,
        superficie INTEGER, 
        id_adresse INTEGER,
        FOREIGN KEY (id_adresse) REFERENCES adresse (id_adresse)
    )
    """)

with open ('image/appart1b.jpg', 'rb') as img1 :
    appart1 = img1.read()

with open('image/appart2.jpg', 'rb') as img2 :
    appart2 = img2.read()

with open('image/appart3.jpg', 'rb') as img3 :
    appart3 = img3.read()

with open('image/appart4.jpg', 'rb') as img4 :
    appart4 = img4.read()

with open('image/appart5.jpg', 'rb') as img5 :
    appart5= img5.read()

with open('image/appart6.jpg', 'rb') as img6 :
    appart6 = img6.read()

with open('image/appart7.jpg', 'rb') as img7 :
    appart7 = img7.read()

with open('image/appart8.jpg', 'rb') as img8 :
    appart8 = img8.read()

with open('image/appart9.jpg', 'rb') as img9 :
    appart9 = img9.read()

with open('image/appart10.jpg', 'rb') as img10 :
    appart10 = img10.read()

with open('image/maison11.jpg', 'rb') as img11 :
    maison11= img11.read()

with open('image/maison12.jpg', 'rb') as img12 :
    maison12 = img12.read()

with open('image/maison13.jpg', 'rb') as img13 :
    maison13 = img13.read()

with open('image/maison14.jpg', 'rb') as img14 :
    maison14 = img14.read()

with open('image/maison15.jpg', 'rb') as img15 :
    maison15 = img15.read()

with open('image/maison16.jpg', 'rb') as img16 :
    maison16 = img16.read()

with open('image/maison17.jpg', 'rb') as img17 :
    maison17 = img17.read()

with open('image/maison18.jpg', 'rb') as img18 :
    maison18 = img18.read()

with open('image/maison19.jpg', 'rb') as img19 :
    maison19 = img19.read()

c.execute("""INSERT INTO logement (titre, description, nb_chambre, type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('Location appartement 2 pièces 42 m²', 'Dans un immeuble ancien, 2/3 pièces de 42.01 m² au 3ème étage comprenant une entrée, un séjour, une chambre, un bureau, une cuisine, un wc séparé et une salle eau.Appartenant rénové, Disponible de suite. Le bien est soumis au statut de la copropriété. Loyer de 1565,00 euros par mois charges comprises dont 65,00 euros par mois de provision pour charge (soumis à la réglementation annuelle)', 1 ,'appartement', 2, 1565, 42, 1)""")
c.execute("""INSERT INTO logement (titre, description, nb_chambre, type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('Location appartement meublé 1 pièce 27 m²', 'Entre père lachaise et voltaire. Nous vous proposons une pièce meublé au troisième étage sans ascenseur. Appartenant comprenant une salle de bains, une cuisine et un séjour. Appartenant entièrement équipé. Disponible immédiatement.', 1, 'appartement', 1, 950, 27, 2)""")
c.execute("""INSERT INTO logement (titre, description, nb_chambre, type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('Location appartement 4 pièces 77 m²', 'EXCLUSIVITE - APPARTEMENT 4 PIECES DANS IMMEUBLE ANCIEN - Venez découvrir cet appartement T4 une surface habitable de 77 mm² à Paris. Un ascenseur est disponible. Il comporte 2 chambres, une cuisine aménagée ainsi que 1 salle de bain. Un chauffage collectif fonctionnant au gaz. Quartier qui contient un très large choix de commerces. Loyer de 1765,00 euros par mois charges comprises dont 165,00 euros par mois de provision pour charges (soumis à la régulation annuelle).', 2, 'appartement', 4, 1765, 77, 3)""")
c.execute("""INSERT INTO logement (titre, description, nb_chambre, type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('Location appartement 5 pièces 110m²', '5 pièces à louer, cave, 1er arrondissement. 110 m², 3ème étage, immeuble ancien, ascenseur, entrée, séjour, salle à manger, 2 chambres, bureau, salle de bain/douche, salle de douche avec WC, WC séparé, cuisine bien équipée, chauffage électrique, cave', 2, 'appartement', 5, 4000, 110, 4  )""")
c.execute("""INSERT INTO logement (titre, description, nb_chambre, type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('Location appartement 5 pièces 141 m²', 'Idéalement situé en plein coeur de Paris à deux pas de la place de la Bourse et de la place des Victoires et à proxmité du Métro Bourse. Dans un bel immeubleancien de standing, sécurisé avec digicode, interphone et gardien. Grand appartement familial de 5 pièces en parfait état au 4ème étage avec ascenseur sans vis-à-vis avec une vue dégagée. Le chauffage et eau chaude sont individuels au gaz.', 3, 'appartement', 4, 3995, 141, 5)""")
c.execute("""INSERT INTO logement (titre, description, nb_chambre, type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('Location appartement 1 pièce 28m²', 'Dans bel immeuble récent avec digicode et interphone - Studio en très bon état de 28m² en rez de chaussée surélevé comprenant une entrée, une pièce principale avec placards, une cuisine aaménagée et partiellement équipée, une salle de bain avec WC. Appartement très clair. En sous-sol une cave et un parking inclus. Le bien est soumis au statut de la copropriété', 1, 'appartement', 1, 890, 28, 6)""")
c.execute("""INSERT INTO logement (titre, description, nb_chambre, type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('Location appartement 5 pièces 115 m²', 'Appartement 5 pièces, dans résidence récente et arborée. Balcons, double exposition, très clair, au 7ème étage comprenant : entrée, Double séjour, 4 chambres cuisine, salle de bains, salle de douches, WC. Cave, Eau chaude, et chauffage compris. Possibilité parking, gardiens. Pas de colocations', 4, 'appartement', 5, 2607, 115, 7)""")
c.execute("""INSERT INTO logement (titre, description, nb_chambre, type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('Location appartement meublé 3 pièces 105 m²', 'Beau 3 pièces meublé, vue , parking, 7e arrondissement. 105 m², 7 étages, immeuble modere, ascenseur, entrée, double, séjour/salle à manger, 2 chambres, salle de bains, salle de douche 2 WC séparés, cuisine bien équipée. Chauffage centrale + eau chaude immeuble, mobilier contemporain, placadrs, double exposition', 2, 'appartement', 3, 3400, 105, 8)""")
c.execute("""INSERT INTO logement (titre, description, nb_chambre, type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('Location appartement meublé 2 pièces 52 m²', 'Appartement meublé, moderne avec belle vue sur jardin intérieur de la résidence très calme situé au 1er étage avec ascenseur. Idéal bail société ou résidence secondaire. Une entrée avec penderie desservant un séjour éclairé par deux portes fenêtres donnant sur un balcon, une belle cuisine américaine totalement équipée, une chambre avec placards intégrés. Terrasse de 7,5 m² permettant de dîner en extérieur avec vue sur jardin privé de la résidence', 1, 'appartement', 2, 1950, 52, 9)""")
c.execute("""INSERT INTO logement (titre, description, nb_chambre, type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('Location appartement 6 pièces 199 m²', 'Bel appartement familiale. Une entrée, une double réception, une cuisine non équipée, de quatre chambres, une salle de bains et de deux salles eau. Placards, dressing. Une cave, chauffrage et eau chaude collectifs. 4884 € par mois charges comprises, donc 500 € de provisions sur charges.', 4, 'appartement', 6, 4884, 199, 10)""")
c.execute("""INSERT INTO logement (titre, description, nb_chambre, type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('Location maison 6 pièces 135m²', 'Maison, excellent état. Maison de 135 m² avec une cour de 35 m². En excellent état et disposant de tout le confort nécessaire, la maison se distribue comme suit sur 4 niveaux de 42 m² au sol. Au Rez-deChaussée, une salle eau avec WC et une chambre conduisant à la cour. Accès au garage contenant un établi. Au 1er étage, pièce de vie transparente et une cuisine semi équipée. Au 2ème, une salle de bain et une chambre. Double vitrage, volets électriques, thermostats.', 2, 'maison', 6, 3600, 135, 11)""")
c.execute("""INSERT INTO logement (titre, description, nb_chambre, type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('Location maison meublée 3 pièces 100m²', 'Maison meublée de 100,8m² environ au Rez-de-chaussée. Elle comporte 1 salon, 2 chambres, 1 cuisine séparée, 1 salle de bain et 1 salle de douche, WC séparés et 1 terrasse. le chauffage est individuel au gaz. A louer pour des périodes de plus de 12 mois.', 2, 'maison', 3, 3200, 100, 12)""")
c.execute("""INSERT INTO logement (titre, description, nb_chambre, type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('Location maison meublée meublée 6 pièces 200 m²', 'Située dans une petite rue très calme de Malakoff. Au Rez-de-Chaussée, un double séjour avec cuisine ouverte et bar américain et une chambre, donnant sur une belle terrasse équipée, une salle eau avec WC. Au 1er, 3 chambres dont une suite parentale équipée de : un WC, une douche, une baignoire, un grand dressing, une salle de bain, et un bureau en mezzanine. Une place de parking et complètent la maison.Le bail proposé est un bail meublé.', 4, 'maison', 6, 3750, 200, 13)""")
c.execute("""INSERT INTO logement (titre, description, nb_chambre, type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('Location maison 5 pièces 111 m²', 'Ce bien rare propose une terrasse de 60m² exposée plein sud, un séjour avec cuisine équipée et aménagée tandis que le premier niveau dessert deux chambres dont une de 6 m², un espace bureau, une salle de bains et une salle eau. Le dernier étahe propose deux chambres accessible par des échelles de meunier. Chauffage et eau chaude individuels au gaz.', 4, 'maison', 5, 3690, 111, 14)""")
c.execute("""INSERT INTO logement (titre, description, nb_chambre, type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('Location maison 4 pièces 76 m²', 'Au calme, dans un quartier pavillonnaire, proche école et transports, maison sousplex en arrière lot en bon état général comprenant séjour, cuisine ouverte aménagée et équipée (hotte et plaque), 2 chambres avec placards, bureau, salle de bains avec WC, salle eau, WC séparé et buanderie. Jardin de 60 m² environ avec cabanon.', 2, 'maison', 4, 1590, 76, 15)""")
c.execute("""INSERT INTO logement (titre, description, nb_chambre, type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('Location maison 8 pièces 153 m²', 'Au coeur du quartier classé du Village Anglais, magnifique maison entièrement rénovée en 2011 comprenant un rez-de-chaussée avec une entrée, 1 WC et un séjour double ouvrant sur une cuisine US aménagée et équipée. Au premier étage, 3 chambres, une salle de bain avec espace buanderie et un WC. Sous les combles, une belle suite parentale avec une salle de bains, dressing et climatisation. Dispose également 1 rez-de-jardin ouvrant sur une belle terrasse exposée sud et comprenant une salle de jeux, 1 chambre et garage.', 5, 'maison', 8, 3900, 153, 16)""")
c.execute("""INSERT INTO logement (titre, description, nb_chambre, type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('Location maison 3 pièces 83 m²', 'Vaste séjour, une cuisine équipée et aménagée (rangements, plaques, four, hottte, frigo), 2 chambres dont une avec un dressing, un dégagement avec placards, une salle de bains et WC séparés, une buanderie, et de nombreux rangements. Un jardinet avec une terrasse.', 2, 'maison', 3, 1299, 83, 17)""")
c.execute("""INSERT INTO logement (titre, description, nb_chambre, type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('Location maison 4 pièces 87 m²', 'Chaleureuse maison familiale de 87, 32 m² au sol combiné aux avantages du confort moderne. Une belle pièce à vivre de plus de 34 m² composé de : 1 espace salon, une salle à manger, une cuisine ouverte aménagée avec accès direct à la terrasse. Deux salles eau avec 3 chambres donnant vue le jardin, un WC séparé, extérieur et jardin de 215 m² et garage fermer.', 3, 'maison', 4, 1911, 87, 18)""")
c.execute("""INSERT INTO logement (titre, description, nb_chambre, type_logement, nb_piece, prix, superficie, id_adresse) VALUES ('Location maison 11 pièces 260 m²', 'Vaste maison de près de 366 m² dont 260 m² habitables, bâtie sur 3 niveaux avec sous-sol. En rez-de-jardin, la double réception offre une jolie vue sur le jardin de 1000 m² clos de murs et aggrandissement sur une véranda lumineuse. Ce niveau comprend également un bureau et une cuisine aménagée. Au premier étage : deux suites. Au deuxième étages: une chambre avec une salle de douche, deux chambres, une salle de bains. Entresole : 3 chambres, une salle eau, un cellier, une buanderie et la chaufferie. Garage deux places et deux emplacements de stationnement extérieurs', 8, 'maison', 11, 5700, 260, 19)""")

c.execute("UPDATE logement SET photo=? WHERE id_logement = 1", (appart1,))
c.execute("UPDATE logement SET photo=? WHERE id_logement = 2", (appart2,))
c.execute("UPDATE logement SET photo=? WHERE id_logement = 3", (appart3,))
c.execute("UPDATE logement SET photo=? WHERE id_logement = 4", (appart4,))
c.execute("UPDATE logement SET photo=? WHERE id_logement = 5", (appart5,))
c.execute("UPDATE logement SET photo=? WHERE id_logement = 6", (appart6,))
c.execute("UPDATE logement SET photo=? WHERE id_logement = 7", (appart7,))
c.execute("UPDATE logement SET photo=? WHERE id_logement = 8", (appart8,))
c.execute("UPDATE logement SET photo=? WHERE id_logement = 9", (appart9,))
c.execute("UPDATE logement SET photo=? WHERE id_logement = 10", (appart10,))
c.execute("UPDATE logement SET photo=? WHERE id_logement = 11", (maison11,))
c.execute("UPDATE logement SET photo=? WHERE id_logement = 12", (maison12,))
c.execute("UPDATE logement SET photo=? WHERE id_logement = 13", (maison13,))
c.execute("UPDATE logement SET photo=? WHERE id_logement = 14", (maison14,))
c.execute("UPDATE logement SET photo=? WHERE id_logement = 15", (maison15,))
c.execute("UPDATE logement SET photo=? WHERE id_logement = 16", (maison16,))
c.execute("UPDATE logement SET photo=? WHERE id_logement = 17", (maison17,))
c.execute("UPDATE logement SET photo=? WHERE id_logement = 18", (maison18,))
c.execute("UPDATE logement SET photo=? WHERE id_logement = 19", (maison19,))

#TABLE DES UTILISATEURS 
c.execute("""
    CREATE TABLE IF NOT EXISTS utilisateur (
        id_utilisateur INTEGER PRIMARY KEY AUTOINCREMENT,
        prenom VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL,
        password VARCHAR(100) NOT NULL,
        pro INTEGER,
        budget INTEGER, 
        temps TIME, 
        id_adresse INTEGER,
        type_logement INTEGER,
        FOREIGN KEY (id_adresse) REFERENCES adresse (id_adresse),
        FOREIGN KEY (type_logement) REFERENCES logement(type_logement)
    )
    """)

c.execute("""INSERT INTO utilisateur (prenom, email, password, budget, temps, id_adresse) VALUES ('Lola', 'lola@gmail.com', 'lola', 2700,'01:00', 19)""")
c.execute("""INSERT INTO utilisateur (prenom, email, password, budget, temps, id_adresse) VALUES ('Damien', 'damien@gmail.com', 'damien', 1900, '00:30', 20) """)
c.execute("""INSERT INTO utilisateur (prenom, email, password, budget, temps, id_adresse) VALUES ('Sarah', 'sarah@gmail.com', 'sarah', 4000, '00:45', 21)""")

password_lola = 'lola'
secure_password_lola = sha256_crypt.hash(password_lola)
c.execute("UPDATE utilisateur SET password=? where id_utilisateur = 1", (secure_password_lola,)) 

password_damien = 'damien'
secure_password_damien = sha256_crypt.hash(password_damien)
c.execute("UPDATE utilisateur SET password=? where id_utilisateur = 2", (secure_password_damien,)) 

password_sarah = 'sarah'
secure_password_sarah = sha256_crypt.hash(password_sarah)
c.execute("UPDATE utilisateur SET password=? where id_utilisateur = 3", (secure_password_sarah,)) 



# TABLE favoris 
c.execute("""
    CREATE TABLE IF NOT EXISTS favoris(
    id_favoris INTEGER PRIMARY KEY AUTOINCREMENT, 
    id_utilisateur INTEGER,
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




