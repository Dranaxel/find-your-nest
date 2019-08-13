from FindYourNest import app, login_manager 
from flask import request, redirect, render_template, flash, url_for, redirect, flash
from flask_login import login_required, UserMixin, login_user, current_user, logout_user
import sqlite3
from passlib.hash import sha256_crypt

conn = sqlite3.connect('findyournest.db', check_same_thread=False)
c = conn.cursor()

# app.secret_key = b'_\x95\xe8\xf1\x80\xe8\x9b\xd3J\x92\x10\xcaLd\x87&'


# #laoding the login manager
@login_manager.user_loader
def load_user(user_id):
    userDansLaBase = c.execute("SELECT email, prenom FROM utilisateur WHERE email=?", (user_id,)).fetchone()
    if userDansLaBase is None:
        return None
    user = UserMixin()
    user.id = user_id
    user.prenom = userDansLaBase[1]
    return user

# # allows to redirect the user to the login page if not authentified
# login_manager.login_view ="/connexion"

@app.route("/")
def main():
    return render_template('index.html')

#se connecter
@app.route("/connexion", methods=["GET", "POST"])
def connexion():
    if request.method =='GET' :
        if current_user.is_anonymous:
            return render_template("connexion.html")
        else :
            flash("Vous êtes déja connecter gros béta")
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
@app.route("/moncompte", methods=["GET", "POST"])
def moncompte():
    if request.method == 'GET' :
        if current_user.is_anonymous:
            return render_template("moncompte.html")
        else:
            flash("Vous êtes déja connecter gros béta")
            return redirect(url_for('main'))

    else :
        
        prenom = request.form['prenom']
        email = request.form['email']
        password = request.form['password']
        confirmer = request.form['confirmer']
        secure_password = sha256_crypt.encrypt(password)
        pro = request.form.getlist('pro')
        nb = request.form['nb']
        rue = request.form['rue']
        ville = request.form['ville']
        code_postal = request.form['code_postal']
        temps = request.form.getlist('temps')
        budget = request.form.get('budget')
        type_logement = request.form.getlist('type_logement')
        

        if not (email and password):
            flash("Il est nécessaire d'entrer un email et un mot de passe", "danger") 
            return render_template("moncompte.html")
        
        elif password == confirmer:
            c.execute("INSERT INTO utilisateur (prenom, email, password, temps) VALUES(?, ?, ?, ?)", (prenom, email, secure_password, temps))
            c.execute("INSERT INTO adresse (nb, rue, ville, code_postal) VALUES(?, ?, ?, ?)", (nb, rue, ville, code_postal,))
            conn.commit()
            return redirect(url_for('connexion'))

        else:
            flash("les mots de passe ne correspondent pas", "danger")
            return render_template("moncompte.html")

#se déconnecter 
@app.route("/deconnexion")
@login_required
def deconnexion():
    logout_user()
    return redirect(url_for('connexion'))
# @app.route("/moncompte/")
# @login_required
# def infocompte():
#     return render_template("infoscompte.html")

# @app.route("/Apt/<int:id>/")
# def aptInfo(id):
#     return render_template("ficheappart.html")

# @app.route("/upAppt/")
# def up_Appt():
#     return render_template("chargementappart.html")

