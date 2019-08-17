from FindYourNest import app, login_manager 
from flask import render_template, request, redirect
from flask_login import login_required
from opencage.geocoder import OpenCageGeocode
from urllib import parse
import sqlite3, requests

#Import Navitia key
navitia_key = app.config['NAVITIA']
navitia_url = "http://api.navitia.io/v1/journeys"

#initializing geocoder wrapper
opencagedata_key = "3c853893fc37402eb2ef1473b6629218"
opencage = OpenCageGeocode(opencagedata_key)

conn = sqlite3.connect('/root/Git/FindYourNest/findyournest.db', check_same_thread=False)
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
	#convert the main address in GPS position with opencau
	opencage_resp = opencage.geocode(add)
	origin_coord = list(opencage_resp[0]['geometry'].values())		
	origin_coord = str(origin_coord[1]) +";"+ str(origin_coord[0])
	
	#convert time in seconds
	max_time = hours*3600 + minutes*60

	#get a list of all the apt in the database
	apt_list = c.execute("select adresse.nb, adresse.rue, adresse.ville, logement.id_logement from adresse inner JOIN logement on logement.id_adresse=adresse.id_adresse").fetchall()
	for ref in apt_list:
		dest_add = ",".join(map(str,ref[:3]))+",FRANCE"
		opencage_resp = opencage.geocode(dest_add, language='fr', no_annotations=1, limit=1, bounds="1.19202,48.41462,3.36182,49.26780")
		dest_coord = list(opencage_resp[0]['geometry'].values())
		dest_coord = str(dest_coord[1])+";"+str(dest_coord[0])
		navitia_param = {'from': origin_coord, "to": dest_coord} 
		navitia_call = requests.get(navitia_url, navitia_param, auth=(navitia_key, ""))
		print(navitia_call.text])
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

#Valeurs checkboxes moncompte
@app.route("/moncompte", methods = ['GET', 'POST'])
def valuescheckboxes(): 
    if request.method == 'POST':
        print (request.method.form.getlist('checkboxlist'))
    return render_template("/moncompte")

