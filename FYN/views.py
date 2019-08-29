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
upload_pro = PurePath ('FYN/ups/')

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
    print(apt_list)
    for ref in apt_list:
        try:
            dest_add = ",".join(map(str,ref[:3]))+",FRANCE"
            opencage_resp = opencage.geocode(dest_add, language='fr', no_annotations=1, limit=1, bounds="1.19202,48.41462,3.36182,49.26780")
            print(opencage_resp)
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
        print(i)
        results.append(c.execute("select titre, prix, photo, description from logement where id_logement=%s"%i).fetchone())
    print(results)
    return render_template("results.html", result= results)

@app.route("/Fiche/<int:id>")
def Fiche(id):
    prix_sql = c.execute("SELECT prix FROM logement WHERE id_logement=?", (id,)).fetchone()
    PostalCode_sql = c.execute("select code_postal from adresse inner JOIN logement on logement.id_adresse=adresse.id_adresse where logement.id_logement= ?", (id,)).fetchone() 
    nb_pieces_sql = c.execute("SELECT nb_piece FROM logement WHERE id_logement=?", (id,)).fetchone()
    surface_sql =  c.execute("SELECT superficie FROM logement WHERE id_logement=?", (id,)).fetchone()
    return render_template("FicheAppart.html", Prix=prix_sql[0], PostalCode=PostalCode_sql[0], nb_pieces=nb_pieces_sql[0], surface=surface_sql[0])

#Partie pro

@app.route("/infoscompte/")
@login_required
def infoscompte():
    if current_user.is_authenticated:
        print(current_user.pro)
        if current_user.pro == 'on':
            email = current_user.id
            infos_pro = c.execute("select prenom, email, temps, budget, maison, appartement, id_utilisateur FROM utilisateur where email=?", (email,)).fetchone()    
            maison = infos_pro[4]
            appartement = infos_pro[5]
            infos_adresse = c.execute("select nb, rue, ville, code_postal from adresse inner join utilisateur on adresse.id_adresse=utilisateur.id_adresse where email=?", (email,)).fetchone()
            if maison == 'on':
                type_logement = 'maison'
            elif appartement == 'on':
                type_logement = 'appartement'
            else:
                type_logement = 'Non précisé'
            return render_template("infoscomptepro.html", prenom=infos_pro[0], email=infos_pro[1], temps=infos_pro[2], budget=infos_pro[3], type_logement=type_logement, nb=infos_adresse[0], rue=infos_adresse[1], ville=infos_adresse[2], code_postal=infos_adresse[3])

        else:
            email =  current_user.id
            infos_pro = c.execute("select prenom, email, temps, budget, maison, appartement, id_utilisateur FROM  utilisateur where email=?", (email,)).fetchone()    
            maison = infos_pro[4]
            appartement = infos_pro[5]
            infos_adresse = c.execute("select nb, rue, ville, code_postal from adresse inner join utilisateur on adresse.id_adresse=utilisateur.id_adresse where email=?", (email,)).fetchone()
            id_user=infos_pro[6]
            infos_favoris = c.execute("SELECT titre, prix, photo, description from logement inner join favoris on logement.id_logement=favoris.id_logement where favoris.id_utilisateur=?", (id_user,)).fetchone()
            if maison == 'on':
                type_logement = 'maison'
            elif appartement == 'on':
                type_logement = 'appartement'
            else:
                type_logement = 'Non précisé'
                return render_template("infoscompte.html", prenom=infos_pro[0], email=infos_pro[1], temps=infos_pro[2], budget=infos_pro[3], type_logement=type_logement, nb=infos_adresse[0], rue=infos_adresse[1], ville=infos_adresse[2], code_postal=infos_adresse[3], titre=infos_favoris[0], prix=infos_favoris[1], photo=infos_favoris[2], description=infos_favoris[3])
    else:
        return redirect(url_for('main'))

def checkextension(namefile):
    """ Renvoie True si le fichier possède une extension d'image valide. """
    print(namefile.rsplit('.', 1)[1])
    return '.' in namefile and namefile.rsplit('.', 1)[1] in ('png', 'jpg', 'jpeg')

@app.route('/infoscompte/', methods=['GET','POST'])
def upload():
    if request.method == 'POST':
            f = request.files['picture']
            if f: # on vérifie qu'un fichier a bien été envoyé
                if checkextension(f.filename): # on vérifie que son extension est valide
                    name = secure_filename(f.filename)
                    f.save(str(upload_pro) + name)
                    flash('Image envoyée !', 'success')
                else:
                    flash('Ce fichier n\'\est pas dans une extension autorisée!', 'error')
            else:
                flash('Vous avez oublié de joindre une image !', 'error')
    else:        
        return render_template('_infoscomptepro_up.html')


@app.route('/views/')
def liste_upped():
    images = [img for img in os.listdir(upload_pro) if checkextension(img)] # la liste des images dans le dossier
    return render_template('_infoscomptepro_liste.html', images=images)


@app.route('/views/<name>')
def upped(name):
    name = secure_filename(name)
    if os.path.isfile(str(upload_pro) + name): # si le fichier existe
        return send_file(str(upload_pro) + name, as_attachment=True) # on l'envoie
    else:
        flash('Fichier {name} inexistant.'.format(name=name), 'error')
        return render_template('liste_upped') # sinon on redirige vers la liste des images, avec un message d'erreur
        
