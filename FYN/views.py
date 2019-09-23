# vim: set ts=4 sw=4 et:
from FYN import app, login_manager 
from flask import send_file, request, redirect, render_template, flash, url_for, redirect, flash
from flask_login import login_required, UserMixin, login_user, current_user, logout_user
from opencage.geocoder import OpenCageGeocode
from urllib import parse
import sqlite3, requests, json
from pathlib import PurePath  
from passlib.hash import sha256_crypt
from werkzeug.utils import secure_filename
from FYN.mail import envoyer_mail, forget_password, contact_mail
import os, logging
from flask import jsonify

#Import Navitia key
navitia_key = app.config['NAVITIA_KEY']
navitia_url = app.config['NAVITIA_URL']


#initializing geocoder wrapper
opencagedata_key = "31dbec8c7f4844a6aafa18c738aea931"
opencage = OpenCageGeocode(opencagedata_key)

database_file = PurePath('./FYN/findyournest.db')
conn = sqlite3.connect(str(database_file), check_same_thread=False)
c = conn.cursor()

#Chargement images dans le dossier
upload_pro = PurePath ('./FYN/ups/')

#loading the login manager
@login_manager.user_loader
def load_user(user_id):
    userDansLaBase = c.execute("SELECT email, prenom, pro FROM utilisateur WHERE email=?", (user_id,)).fetchone()
    if userDansLaBase is None:
        return None
    user = UserMixin()
    user.id = user_id
    user.prenom = userDansLaBase[1]
    user.pro = userDansLaBase[2]
    return user


@app.route("/", methods=["GET", "POST"])
def main():
    if request.method == "GET":
        if current_user.is_authenticated:
            if current_user.pro == 'on' : 
                return render_template('index.html')
            else:
                adresse_user = c.execute('SELECT nb, rue, code_postal, ville FROM adresse a join utilisateur u on a.id_adresse=u.id_adresse where email=?', (current_user.id,)).fetchone()
                nb_user = adresse_user[0]
                rue_user = adresse_user[1]
                ville_user = adresse_user[3]
                code_postal_user = adresse_user[2]
                user_adresse = str(nb_user) + ' ' + rue_user + ' ' + str(code_postal_user) + ' ' + ville_user
                temps_user = c.execute('SELECT temps from utilisateur where email=?', (current_user.id,)).fetchone()
                user_temps = temps_user[0]
                temps_split = user_temps.split(':')
                h = temps_split[0]
                min = temps_split[1]
                return render_template('index.html', user_adresse=user_adresse, h=h, min=min)
        else : 
            return render_template('index.html')
            
    elif request.method =="POST":
        #get response from the form
        address = request.form['addresse']
        hours = request.form['hours']
        minutes = request.form['minutes']
        #return the result page pasing the arguments
        return redirect("/results/add="+address+"&h="+hours+"&m="+minutes)

#se connecter
@app.route("/connexion/", methods=["GET", "POST"])
def connexion():
    if request.method =='GET' :
        if current_user.is_anonymous:
            return render_template("connexion.html")
        else :
            return redirect(url_for('main'))
    
    elif request.method =='POST':
        email = request.form['email']
        password = request.form['password']

        results = c.execute("SELECT prenom, password FROM utilisateur WHERE email=?", (email,)).fetchone()
        

        if results :
            passwordEnBase = results[1]
            if sha256_crypt.verify(password, passwordEnBase):
                user = UserMixin()
                user.id = email
                user.prenom = results[0]
                login_user(user)
                return redirect(url_for('main'))
            else:
                flash("Votre email et/ou votre mot de passe est incorrect. Veuillez les saisir à nouveau ", "danger")
                return render_template("connexion.html")
        
        else :
            flash("Votre email et/ou votre mot de passe est incorrect. Veuillez les saisir à nouveau ", "danger")
            return render_template("connexion.html")

#envoie du mail pour réinialiser le mot de passe 
@app.route("/mail_reinitiate_pwd/", methods=["GET", "POST"])
def mail_reinitiate_pwd():
    if request.method == 'GET':
        if current_user.is_anonymous:
            return render_template("mail_pwd.html")
        else:
            return redirect(url_for('main'))
    else:
        email = request.form['email']

        user_mail = c.execute("SELECT prenom FROM utilisateur where email=?", (email,)).fetchone()
        if user_mail is not None :
            prenom = user_mail[0]
            forget_password(email, prenom)
            flash("Le mail a bien été envoyé ! ", "success")
            return redirect(url_for('connexion'))
        else:
            flash("Cet email n'est pas attribué ! Veuillez en entrer une nouvelle !", "danger")
            return render_template("mail_pwd.html")

#reinitialisation du mot de passe 
@app.route("/reinitialisation_pwd/", methods=["GET", "POST"])
def reinialisation_pwd():
    if request.method == 'GET':
        if current_user.is_anonymous:
            return render_template("reinitialisation.html")
        else:
            return redirect(url_for('main'))
    else:
        email = request.form['email']
        password = request.form['password']
        confirmer = request.form['confirmer']
        secure_password = sha256_crypt.encrypt(password)

        user = c.execute("SELECT * FROM utilisateur where email=?", (email,)).fetchone()
        if user is None:
            flash("Cet email n'est pas attribué ! Veuillez en entrer une nouvelle !", "danger")
            return render_template("reinitialisation.html")
        else:
            if password == confirmer :
                c.execute("UPDATE utilisateur SET password=? WHERE email=?", (secure_password, email,))
                conn.commit()
                flash("Le mot de passe a bien été enregistré", "success")
                return redirect(url_for('connexion'))
            else:
                flash("Les mots de passes ne correspondent pas ! Veuillez resaisir les mots de passe ! ", "danger")
                return render_template("reinitialisation.html")
      
#créer le compte
@app.route("/moncompte/", methods=["GET", "POST"])
def moncompte():
    if request.method == 'GET' :
        if current_user.is_anonymous:
            return render_template("moncompte.html")
        else:
            return redirect(url_for('main'))

    else :
        prenom = request.form['prenom']
        email = request.form['email']
        password = request.form['password']
        confirmer = request.form['confirmer']
        secure_password = sha256_crypt.encrypt(password)
        pro = request.form.get('pro')
        nb = request.form['nb']
        rue = request.form['rue']
        ville = request.form['ville']
        code_postal = request.form['code_postal']
        temps = request.form.get('temps')
        budget = request.form.get('budget')
        maison = request.form.get('maison')
        appart = request.form.get('appart')

        if not (email and password):
            flash("Il est nécessaire d'entrer un email et un mot de passe", "danger") 
            return render_template("moncompte.html")
        elif password == confirmer:
            adress = c.execute("SELECT rue, nb, ville FROM adresse where nb=? and rue=? and ville=?", (nb, rue, ville,)).fetchone()
            one_user = c.execute("SELECT * FROM utilisateur where email=?", (email,)).fetchone()
            if one_user is not None:
                flash("L'adresse email est déjà utilisée ! Veuillez en entrer une autre ! ", "danger")
                return render_template("moncompte.html")
            else:
                c.execute("INSERT INTO utilisateur (prenom, email, password, pro, temps, budget, maison, appartement) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (prenom, email, secure_password, pro, temps, budget, maison, appart,))
                conn.commit()
                adress = c.execute("SELECT id_adresse FROM adresse where nb=? and rue=? and ville=?", (nb, rue, ville,)).fetchone()

                if adress is None:
                    c.execute("INSERT INTO adresse (nb, rue, ville, code_postal) VALUES(?,?,?,?)", (nb, rue, ville, code_postal,))
                    conn.commit()
                    c.execute("delete from adresse where nb='' AND rue='' AND ville='' AND code_postal=''")
                    conn.commit()
                    id_adres = c.execute("SELECT id_adresse FROM adresse WHERE nb=? AND rue=? AND ville=?", (nb, rue, ville,)).fetchone()
                    if id_adres is not None :
                        id_adresse = id_adres[0]
                        c.execute("UPDATE utilisateur SET id_adresse=? WHERE email=?", (id_adresse, email,))
                        conn.commit() 
                else:
                    id_adresse = id_adres[0]
                    c.execute("UPDATE utilisateur SET id_adresse=? WHERE email=?", (id_adresse, email,))
                    conn.commit()
                envoyer_mail(email,prenom)    
                return redirect(url_for('connexion'))
        else:
            flash("Les mots de passe ne correspondent pas", "danger")
            return render_template("moncompte.html")


#se déconnecter 
@app.route("/deconnexion")
@login_required
def deconnexion():
    logout_user()
    return redirect(url_for('connexion'))


@app.route("/results/add=<string:add>&h=<int:hours>&m=<int:minutes>", methods=["GET", "POST"])
def aptInfo(add,hours,minutes):
    if request.method == 'GET':
        saved_ref =[]
        results = []
        #convert the main address in GPS position with opencau
        opencage_resp = opencage.geocode(add)
        origin_coord = list(opencage_resp[0]['geometry'].values())      
        origin_coord = str(origin_coord[1]) +";"+ str(origin_coord[0])

        #convert time in seconds
        max_time = hours*3600 + minutes*60

        #get a list of all the apt in the database
        apt_list = c.execute("select adresse.nb, adresse.rue, adresse.ville, logement.id_logement from adresse inner JOIN logement on logement.id_adresse=adresse.id_adresse").fetchall()
        for ref in apt_list:
            try:
                dest_add = ",".join(map(str,ref[:3]))+",FRANCE"
                opencage_resp = opencage.geocode(dest_add, language='fr', no_annotations=1, limit=1, bounds="1.19202,48.41462,3.36182,49.26780")
                dest_coord = list(opencage_resp[0]['geometry'].values())
                dest_coord = str(dest_coord[1])+";"+str(dest_coord[0])
                navitia_param = {'from': origin_coord, 'to': dest_coord}
                logging.exception(navitia_param)
                navitia_call = requests.get(navitia_url, data = navitia_param, auth=(navitia_key, ""))
                navitia_call = json.loads(navitia_call.text)
                duration = navitia_call['journeys'][0]["duration"]
            except:
                print("error")
                continue
            if duration <=  max_time:
                saved_ref.append(ref[3])
        for i in saved_ref:
            results.append(c.execute("select titre, prix, photo, description, id_logement from logement where id_logement=%s"%i).fetchone())
        return render_template("results.html", result= results)

@app.route("/getFavorite/<int:id>", methods=['POST'])
def getFavorite(id):
    id_logement = id
    # logement_sql = c.execute("SELECT id_logement FROM logement WHERE id_logement=?", (id_logement,)).fetchone()
    # id_log=logement_sql[0]
    # favoris_log = request.form.get('log_fav')
    id_user = c.execute("SELECT id_utilisateur FROM utilisateur where email=?", (current_user.id,)).fetchone()
    id_utilisateur = id_user[0]
    id_fav = c.execute("SELECT * FROM favoris where id_utilisateur=? and id_logement=?", (id_utilisateur, id_logement,)).fetchone()
    # if favoris_log == 'on':
    if id_fav is not None :
        response = {
            "is": False,
            "msg": "L'annonce se trouve déjà dans vos favoris !"
        }
    else:
        c.execute("INSERT INTO favoris(id_logement, id_utilisateur) VALUES(? , ?)", (id_logement, id_utilisateur,))
        conn.commit()
        response = {
            "is": True,
            "msg": "L'annonce a bien été ajouté dans vos favoris"
        }
   
    return jsonify(response)

@app.route("/Fiche/<int:id>", methods=["GET","POST"])
def Fiche(id):
    if request.method == 'GET':
        titre_sql = c.execute("SELECT titre FROM logement where id_logement=?", (id,)).fetchone()
        nb_chambre_sql = c.execute("SELECT nb_chambre FROM logement where id_logement=?", (id,)).fetchone()
        prix_sql = c.execute("SELECT prix FROM logement WHERE id_logement=?", (id,)).fetchone()
        PostalCode_sql = c.execute("select code_postal from adresse inner JOIN logement on logement.id_adresse=adresse.id_adresse where logement.id_logement= ?", (id,)).fetchone() 
        nb_pieces_sql = c.execute("SELECT nb_piece FROM logement WHERE id_logement=?", (id,)).fetchone()
        surface_sql =  c.execute("SELECT superficie FROM logement WHERE id_logement=?", (id,)).fetchone()
        describe_sql = c.execute("SELECT description FROM logement where id_logement=?", (id,)).fetchone()
        pic_sql = c.execute("SELECT photo FROM logement where id_logement=?", (id,)).fetchone()
        return render_template("FicheAppart.html", titre=titre_sql[0], nb_chambre=nb_chambre_sql[0], Prix=prix_sql[0], PostalCode=PostalCode_sql[0], nb_pieces=nb_pieces_sql[0], surface=surface_sql[0], describe= describe_sql[0], pic=pic_sql[0])

    else : 
        if 'add_favorites' in request.form:
            logement_sql = c.execute("SELECT id_logement FROM logement WHERE id_logement=?", (id,)).fetchone()
            id_log=logement_sql[0]
            # favoris_log = request.form.get('log_fav')
            id_user = c.execute("SELECT id_utilisateur FROM utilisateur where email=?", (current_user.id,)).fetchone()
            id_utilisateur = id_user[0]
            id_fav = c.execute("SELECT * FROM favoris where id_utilisateur=? and id_logement=?", (id_utilisateur, id,)).fetchone()
            print(id)
            # if favoris_log == 'on':
            if id_fav is not None : 
                flash("Le logement est déjà dans vos favoris !", "danger")
                return redirect(url_for('Fiche', id=id_log))

            else:
                c.execute("INSERT INTO favoris(id_logement, id_utilisateur) VALUES(? , ?)", (id, id_utilisateur))
                conn.commit()
                return redirect(url_for('main'))
        
        elif 'contact' in request.form:
            user_prenom = request.form['prenom']
            user_email = request.form['email']
            user_number = request.form['phonenumber']
            user_msg = request.form['message']

            if not user_email : 
                titre = c.execute("SELECT titre, id_logement from logement where id_logement=?", (id,)).fetchone()
                id_log = titre[1]
                flash("Il est nécessaire d'entrer une adresse email !", "danger")
                return redirect(url_for('Fiche', id=id_log))
            else:
                titre = c.execute("SELECT titre, id_logement from logement where id_logement=?", (id,)).fetchone()
                title = titre[0]
                id_log = titre[1]

                pro_mail = c.execute("SELECT email, prenom from utilisateur u join bien b on u.id_utilisateur=b.id_utilisateur join logement l on b.id_logement=l.id_logement where l.id_logement=?", (id,)).fetchone()
                pro_email = pro_mail[0]
                pro_prenom = pro_mail[1]
                contact_mail(user_prenom, user_email, user_number, user_msg, pro_email, pro_prenom, title)
                return redirect(url_for('Fiche', id=id_log))

            
#Partie pro
@app.route("/infoscompte/", methods=["GET", "POST"])
@login_required
def infoscompte(): 
    if request.method == 'GET':
        if current_user.pro == 'on':
            infos = c.execute("select prenom, email, temps, budget, nb, ville, code_postal, rue FROM  utilisateur JOIN adresse on utilisateur.id_adresse=adresse.id_adresse where email=?", (current_user.id,)).fetchall()
            return render_template("infoscompte.html", infos=infos)
        else:
            infos_user = c.execute("SELECT maison, appartement, id_adresse FROM  utilisateur where email=?", (current_user.id,)).fetchone()
            maison = infos_user[0]
            appartement = infos_user[1]
            if maison == 'on':
                type_logement = 'maison'
            elif appartement == 'on':
                type_logement = 'appartement'
            else:
                type_logement = 'Non précisé'
            infos = []
            info_favoris = []
            #infos utilisateur
            infos = c.execute("select prenom, email, temps, budget, nb, ville, code_postal, rue FROM  utilisateur JOIN adresse on utilisateur.id_adresse=adresse.id_adresse where email=?", (current_user.id,)).fetchall()
            # info_favoris = c.execute("SELECT titre, prix, photo, description from logement join favoris on logement.id_logement=favoris.id_logement where favoris.id_utilisateur=?", (apt_ref,)).fetchone()
            info_favoris = c.execute("select titre, prix, photo, description, l.id_logement from logement as l join favoris as f on f.id_logement = l.id_logement join utilisateur as u on u.id_utilisateur = f.id_utilisateur where u.email=?", (current_user.id,)).fetchall()
            if info_favoris is None: 
                return render_template("infoscompte.html", infos=infos, type_logement=type_logement)
            else:
                return render_template("infoscompte.html", infos=infos, infos_favoris=info_favoris, type_logement=type_logement)

#partie pour update les informations
    else:
        #modification des informations utilisateur
        if 'infos_user' in request.form:
            new_prenom = request.form['prenom']
            new_nb = request.form['nb']
            new_rue = request.form['rue']
            new_ville = request.form['ville']
            new_code_postal = request.form['code_postal']
            new_budget = request.form.get('budget')
            infos_user = c.execute("SELECT email FROM utilisateur where email=?", (current_user.id,)).fetchone()
            infos_adresse = c.execute("SELECT nb, rue, ville, code_postal FROM adresse where nb=? and rue=? and ville=? and code_postal=?", (new_nb, new_rue, new_ville, new_code_postal,)).fetchone()

            if infos_adresse is None:
                c.execute("INSERT INTO adresse (nb, rue, ville, code_postal) VALUES(?, ?, ?, ?)", (new_nb, new_rue, new_ville, new_code_postal,))
                conn.commit()
                c.execute("DELETE FROM adresse WHERE nb IS NULL AND rue IS NULL AND ville IS NULL")
                conn.commit()
                id_adres= c.execute("SELECT id_adresse FROM adresse WHERE nb=? AND rue=? AND ville=?", (new_nb, new_rue, new_ville,)).fetchone()
                id_adresse = id_adres[0]
                c.execute("UPDATE utilisateur SET prenom=?, budget=?, id_adresse=? where email=?", (new_prenom, new_budget, id_adresse, current_user.id,))
                conn.commit()     
                return redirect(url_for('infoscompte'))

            else : 
                id_adres= c.execute("SELECT id_adresse FROM adresse WHERE nb=? AND rue=? AND ville=?", (new_nb, new_rue, new_ville,)).fetchone()
                id_adresse = id_adres[0]
                c.execute("UPDATE utilisateur SET prenom=?, budget=?, id_adresse=? where email=?",(new_prenom, new_budget, id_adresse, current_user.id,))
                conn.commit()
                print(id_adres)
                return redirect(url_for('infoscompte'))
        
        # suppresion des favoris
        elif 'del_fav' in request.form: 
            id_logement = request.form.get('del_fav')
            id_user = c.execute("SELECT id_utilisateur FROM utilisateur where email=?", (current_user.id,)).fetchone()
            id_utilisateur = id_user[0]
            c.execute("DELETE FROM favoris where id_logement=? and id_utilisateur=?", (id_logement, id_utilisateur,))    
            conn.commit()
            return redirect(url_for('infoscompte'))

        #upload d'image 
        elif 'uploadbien' in request.form:
            registerbien()
            return redirect(url_for('infoscompte'))


#Enregistrement données du bien pro
def registerbien():
    titre = request.form['titre']
    nb = request.form['nb']
    rue = request.form['rue']
    ville = request.form['ville']
    code_postal = request.form['code_postal']
    description = request.form['description']
    superficie = request.form['superficie']
    nb_chambre = request.form['nb_chambre']
    maison = request.form.get('maison')
    appart = request.form.get('appart')
    prix = request.form['prix']
    f = request.files['photo']

    id_user=c.execute("SELECT id_utilisateur FROM utilisateur WHERE email=?", (current_user.id,)).fetchone()
    id_utilisateur=id_user[0]

    logement_ex=c.execute("SELECT * from logement l join adresse a on l.id_adresse=a.id_adresse where nb=? and rue=? and ville=? and code_postal=?", (nb, rue, ville, code_postal,)).fetchone()
    
    if f: # on vérifie qu'un fichier a bien été envoyé
        if checkextension(f.filename): # on vérifie que son extension est valide
            name=secure_filename(f.filename)
            f.save(os.path.join('./FYN/static/image', name))
            photo = 'image/'+ name
            print(photo)

            if logement_ex is not None :
                flash('Cet adresse est déjà attribué à un logement', 'danger')
                return render_template('infoscompte.html')
            else:
                # insertion de l'adresse
                c.execute("INSERT INTO logement(titre, description, nb_chambre, prix, superficie, maison, appartement) VALUES(?, ?, ?, ?, ?, ?, ?)", (titre, description, nb_chambre, prix, superficie, maison, appart,))
                conn.commit()
                c.execute("INSERT INTO adresse(nb, rue, code_postal, ville) VALUES(?,?,?,?)", (nb, rue, code_postal, ville,))
                conn.commit()
                id_ad=c.execute("SELECT * FROM adresse where nb=? and rue=? and code_postal=? and ville=?", (nb, rue, code_postal, ville,)).fetchone()
                id_adresse=id_ad[0]
                c.execute("UPDATE logement SET id_adresse=? where titre=? and description=? and prix=? and nb_chambre=?", (id_adresse, titre, description, prix, nb_chambre,))
                conn.commit()
                c.execute("UPDATE logement SET photo=? where titre=? and description=? and prix=? and nb_chambre=?", (photo, titre, description, prix, nb_chambre,))
                conn.commit()
                
                id_log=c.execute("SELECT * FROM logement WHERE titre=? AND description=? AND nb_chambre=? AND prix=? AND superficie=?", (titre, description, nb_chambre, prix, superficie,)).fetchone()
                id_loge=id_log[0]
                c.execute("INSERT INTO bien(id_logement, id_utilisateur) VALUES(?, ?)", (id_loge, id_utilisateur,))
                conn.commit()

                type_loge=c.execute("select maison, appartement from logement where id_logement=?", (id_loge,)).fetchone()
                maison = type_loge[0]
                appartement = type_loge[1]
                if maison == 'on':
                    c.execute("UPDATE logement SET type_logement=? where id_logement=?", ('maison', id_loge,))
                    conn.commit()
                elif appartement == 'on':
                    c.execute("UPDATE logement SET type_logement=? where id_logement=?", ('appartement', id_loge,))
                    conn.commit()
                else:
                    pass
                flash ('Votre bien a été enregistré' , 'success')
                return redirect(url_for('infoscompte'))
        else:
            flash('Ce fichier n\'est pas dans une extension autorisée!', 'danger')
            return render_template("infoscompte.html")
    else:
        flash('Vous avez oublié de joindre une image !', 'danger')
        return render_template('infoscompte.html')

def checkextension(namefile):
    print(namefile.rsplit('.', 1)[1])
    return '.' in namefile and namefile.rsplit('.', 1)[1] in ('png', 'jpg', 'jpeg')


