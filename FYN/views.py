# vim: set ts=4 sw=4 et:
from FYN import app, login_manager 
from flask import send_file, request, redirect, render_template, flash, url_for, redirect, flash
from flask_login import login_required, UserMixin, login_user, current_user, logout_user
from opencage.geocoder import OpenCageGeocode
from urllib import parse
import sqlite3, requests, json
from pathlib import PurePath  
from passlib.hash import sha256_crypt
from werkzeug import secure_filename
from werkzeug.utils import secure_filename

#Import Navitia key
navitia_key = app.config['NAVITIA']
navitia_url = "http://api.navitia.io/v1/journeys"

#initializing geocoder wrapper
opencagedata_key = "3c853893fc37402eb2ef1473b6629218"
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
            if adress is None:
                c.execute("INSERT INTO adresse (nb, rue, ville, code_postal) VALUES(?,?,?,?)", (nb, rue, ville, code_postal,))
                conn.commit()
                c.execute("DELETE FROM adresse WHERE nb IS NULL AND rue IS NULL AND ville IS NULL")
                conn.commit()
                
                one_user = c.execute("SELECT * FROM utilisateur where email=?", (email,)).fetchone()
                id_adres = c.execute("SELECT id_adresse FROM adresse WHERE nb=? AND rue=? AND ville=?", (nb, rue, ville,)).fetchone()
                id_adresse = id_adres[0]
                
                if one_user is not None:
                    flash("L'adresse email est déjà utilisée ! Veuiller en entrez une autre ! ", "danger")
                    return render_template("moncompte.html")
                
                elif one_user is None:
                    c.execute("INSERT INTO utilisateur (prenom, email, password, pro, temps, budget, maison, appartement) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (prenom, email, secure_password, pro, temps, budget, maison, appart,))
                    conn.commit()
                    c.execute("UPDATE utilisateur SET id_adresse=? WHERE email=?", (id_adresse, email,))
                    conn.commit()
            else:
                one_user = c.execute("SELECT * FROM utilisateur where email=?", (email,)).fetchone()
                id_adres = c.execute("SELECT id_adresse FROM adresse WHERE nb=? AND rue=? AND ville=?", (nb, rue, ville,)).fetchone()
                id_adresse = id_adres[0]
                if one_user is not None:
                    flash("L'adresse email est déjà utilisée ! Veuiller en entrez une autre ! ", "danger")
                    return render_template("moncompte.html")
                
                elif one_user is None:
                    c.execute("INSERT INTO utilisateur (prenom, email, password, pro, temps, budget, maison, appartement) VALUES(?, ?, ?, ?, ?, ?, ?, ?)", (prenom, email, secure_password, pro, temps, budget, maison, appart,))
                    conn.commit()
                    c.execute("UPDATE utilisateur SET id_adresse=? WHERE email=?", (id_adresse, email,))
                    conn.commit()
                    
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


@app.route("/results/add=<string:add>&h=<int:hours>&m=<int:minutes>")
def aptInfo(add,hours,minutes):
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
            navitia_param = {'from': origin_coord, "to": dest_coord} 
            navitia_call = requests.get(navitia_url, navitia_param, auth=(navitia_key, ""))
            navitia_call = json.loads(navitia_call.text)
            duration = navitia_call['journeys'][0]["duration"]
        except:
            print("error")
            continue
        if duration <=  max_time:
            saved_ref.append(ref[3])
    for i in saved_ref:
        results.append(c.execute("select titre, prix, photo, description from logement where id_logement=%s"%i).fetchone())
    return render_template("results.html", result= results)

@app.route("/Fiche/<int:id>")
def Fiche(id):
    prix_sql = c.execute("SELECT prix FROM logement WHERE id_logement=?", (id,)).fetchone()
    PostalCode_sql = c.execute("select code_postal from adresse inner JOIN logement on logement.id_adresse=adresse.id_adresse where logement.id_logement= ?", (id,)).fetchone() 
    nb_pieces_sql = c.execute("SELECT nb_piece FROM logement WHERE id_logement=?", (id,)).fetchone()
    surface_sql =  c.execute("SELECT superficie FROM logement WHERE id_logement=?", (id,)).fetchone()
    return render_template("FicheAppart.html", Prix=prix_sql[0], PostalCode=PostalCode_sql[0], nb_pieces=nb_pieces_sql[0], surface=surface_sql[0])

#Partie pro

@app.route("/infoscompte/", methods=["GET", "POST"])
@login_required
def infoscompte(): 
    if request.method == 'GET':
        if current_user.is_authenticated:
            #utilisateur normal
            if current_user.pro is None: 
                infos_user = c.execute("SELECT maison, appartement FROM  utilisateur where email=?", (current_user.id,)).fetchone()
                maison = infos_user[0]
                appartement = infos_user[1]
                
                id_rue = c.execute("SELECT rue FROM adresse a join utilisateur u on a.id_adresse=u.id_adresse where email=?", (current_user.id,)).fetchone()
                rue = id_rue[0]
                print(rue)

                if maison == 'on':
                    type_logement = 'maison'
                elif appartement == 'on':
                    type_logement = 'appartement'
                else:
                    type_logement = 'Non précisé'

                infos = []
                info_favoris = []

                #infos utilisateur
                infos = c.execute("select prenom, email, temps, budget, nb, ville, code_postal FROM  utilisateur JOIN adresse on utilisateur.id_adresse=adresse.id_adresse where email=?", (current_user.id,)).fetchall()

                # info_favoris = c.execute("SELECT titre, prix, photo, description from logement join favoris on logement.id_logement=favoris.id_logement where favoris.id_utilisateur=?", (apt_ref,)).fetchone()
                info_favoris = c.execute("select titre, prix, photo, description from logement as l join favoris as f on f.id_logement = l.id_logement join utilisateur as u on u.id_utilisateur = f.id_utilisateur where u.email=?", (current_user.id,)).fetchall()

                if info_favoris is None: 
                    return render_template("infoscompte.html", infos=infos, type_logement=type_logement, rue=rue)
                    
                else:
                    
                    return render_template("infoscompte.html", infos=infos, infos_favoris=info_favoris, type_logement=type_logement, rue=rue)
            # #partie pro
            # else:
            #     email = current_user.id
            #     infos_pro = c.execute("select prenom, email, temps, budget, maison, appartement, id_utilisateur FROM utilisateur where email=?", (email,)).fetchone()    
            #     maison = infos_pro[4]
            #     appartement = infos_pro[5]
            #     infos_adresse = c.execute("select nb, rue, ville, code_postal from adresse inner join utilisateur on adresse.id_adresse=utilisateur.id_adresse where email=?", (email,)).fetchone()
            #     if maison == 'on':
            #         type_logement = 'maison'
            #     elif appartement == 'on':
            #         type_logement = 'appartement'
            #     else:
            #         type_logement = 'Non précisé'
            #     return render_template("infoscomptepro.html", prenom=infos_pro[0], email=infos_pro[1], temps=infos_pro[2], budget=infos_pro[3], type_logement=type_logement, nb=infos_adresse[0], rue=infos_adresse[1], ville=infos_adresse[2], code_postal=infos_adresse[3])


        #partie pour update les informations
    elif request.form == 'POST':
        new_prenom = request.form['prenom']
        new_email = request.form['email']
        new_nb = request.form['nb']
        new_rue = request.form['rue']
        new_ville = request.form['ville']
        new_code_postal = request.form['code_postal']
        new_budget = request.form.get('budget')
        
        cur_user = c.execute("SELECT id_utilisateur from utilisateur where email=?", (current_user.id,)).fetchone()
        id_current = cur_user[0]

        infos_user = c.execute("SELECT email FROM utilisateur where email=?", (new_email,)).fetchone()
        infos_adresse = c.execute("SELECT nb, rue, ville, code_postal FROM adresse where nb=? and rue=? and ville=? and code_postal=?", (new_nb, new_rue, new_ville, new_code_postal,)).fetchone()

        #Eviter que lors de l'update l'utilisateur entre un utilisateur déjà existant                
        if infos_user is not None :
            flash("Cette email est déjà utilisé !", "danger")

        else:
            #adresse non existant     
            if infos_adresse is None:
                c.execute("INSERT INTO adresse (nb, rue, ville, code_postal) VALUES(%s,%s,%s,%s)", (new_nb, new_rue, new_ville, new_code_postal,))
                conn.commit()
                c.execute("DELETE FROM adresse WHERE nb IS NULL AND rue IS NULL AND ville IS NULL")
                conn.commit()
                #récupérer l'id_adresse
                id_adres= c.execute("SELECT id_adresse FROM adresse WHERE nb=%s AND rue=%s AND ville=%s", (new_nb, new_rue, new_ville,)).fetchone()
                id_adresse = id_adres[0]

                c.execute("UPDATE utilisateur SET email=replace(?,?) and budget=? and prenom=? and id_adresse=? where id_utilisateur=?", (current_user.id, new_email, new_budget, new_prenom, id_adresse, id_current,))
                conn.commit()
                return redirect(url_for('infoscompte'))

            else:
                c.execute("UPDATE utilisateur SET email=replace(?,?) and budget=? and prenom=? and id_adresse=? where id_utilisateur=?",(current_user.id, new_email, new_budget, new_prenom , id_adresse, id_current,))
                conn.commit()
                return redirect(url_for('infoscompte'))
                    
    else:
        return redirect(url_for('main'))
    
@app.route('/infoscompte/', methods=['GET','POST'])
def checkextension(namefile):
    """ Renvoie True si le fichier possède une extension d'image valide. """
    print(namefile.rsplit('.', 1)[1])
    return '.' in namefile and namefile.rsplit('.', 1)[1] in ('png', 'jpg', 'jpeg')

def upload():
    if request.method == 'POST':
            f = request.files['picture']
            if f: # on vérifie qu'un fichier a bien été envoyé
                if checkextension(f.filename): # on vérifie que son extension est valide
                    name = secure_filename(f.filename)
                    f.save(os.path.join('./FYN/static/ups', name))
                    flash ('Image enregistrée', 'success')
                else:
                    flash('Ce fichier n\'est pas dans une extension autorisée!', 'error')
            else:
                flash('Vous avez oublié de joindre une image !', 'error')
    else:               
        return render_template('infoscomptepro.html', name=name)
