from FindYourNest import app, login_manager 
from flask import render_template, request, redirect
from flask_login import login_required
import sqlite3, requests

#Import Navitia key
navitia_key = app.config.NAVITIA
navitia_url = http://api.navitia.io/

conn = sqlite3.connect('../findyournest.db', check_same_thread=False)
c = conn.cursor()

#loading the login manager
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# allows to redirect the user to the login page if not authentified
login_manager.login_view ="/connexion"

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

@app.route("/connexion/")
def connexion():
    return render_template("connexion.html")

@app.route("/moncompte/")
@login_required
def infocompte():
    return render_template("infoscompte.html")

@app.route("/results/add=<string:add>&h=<int:hours>&m=<int:minutes>")
def aptInfo(add,hours,minutes):
	return render_template("results.html")

@app.route("/Fiche/<int:id>")
def Fiche(id):
    prix_sql = c.execute("SELECT prix FROM logement WHERE id_logement=?", (id,)).fetchone()
    PostalCode_sql = c.execute("select code_postal from adresse inner JOIN logement on logement.id_adresse=adresse.id_adresse where logement.id_logement= ?", (id,)).fetchone() 
    nb_pieces_sql = c.execute("SELECT nb_piece FROM logement WHERE id_logement=?", (id,)).fetchone()
    surface_sql =  c.execute("SELECT superficie FROM logement WHERE id_logement=?", (id,)).fetchone()

    return render_template("FicheAppart.html", Prix=prix_sql[0], PostalCode=PostalCode_sql[0], nb_pieces=nb_pieces_sql[0], surface=surface_sql[0])

@app.route("/upAppt/")
def up_Appt():
    return render_template("chargementappart.html")

