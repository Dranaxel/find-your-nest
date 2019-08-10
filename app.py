#!/usr/bin/env python3

from flask import Flask, request, redirect, render_template, session, logging, url_for, flash 
import sqlite3

#crypter le mot de passe
from passlib.hash import sha256_crypt

#connexion avec la base de données
conn = sqlite3.connect('findyournest.db', check_same_thread=False)
c = conn.cursor()

app = Flask(__name__, static_folder="templates", static_url_path="")
app.secret_key = b'1234567890'

#page d'accueil 
@app.route("/")
def home():
    return render_template("connexion.html")

# pour créer un compte    
@app.route("/moncompte", methods=["GET", "POST"])
def moncompte():
    if request.method == 'GET' :
        return render_template("moncompte.html")

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
            flash("Il est nécessaire d'entrer un email ou un mot de passe") 
            return render_template("moncompte.html")
        
        elif password == confirmer:
            c.execute("INSERT INTO utilisateur (prenom, email, password) VALUES(?, ?, ?)", (prenom, email, password,))
            c.execute("INSERT INTO adresse (nb, rue, ville, code_postal) VALUES(?, ?, ?, ?)", (nb, rue, ville, code_postal,))
            conn.commit()
            return redirect(url_for('connexion'))

        else:
            flash("les mots de passe ne correspondent pas", "danger")
            return render_template("moncompte.html")


#pour se connecter 
@app.route("/connexion", methods=["GET", "POST"])
def connexion():
    if request.method =='GET' :
        return render_template("connexion.html")
    
    elif request.method =='POST':
        email = request.form['email']
        password = request.form['password']

        results = c.execute("SELECT * FROM utilisateur WHERE email=? AND password=?", (email, password,)).fetchall()
        

        if results :
            for i in results:
                flash ("You are login", "success")
                return ("Vous êtes maitenant connecté")
        
        else :
            flash("L'email ou le mot de passe de sont pas reconnu", "danger")
            return render_template("connexion.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)


