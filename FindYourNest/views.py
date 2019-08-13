from FindYourNest import app, login_manager 
from flask import render_template
from flask_login import login_required

#laoding the login manager
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

# allows to redirect the user to the login page if not authentified
login_manager.login_view ="/connexion"

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/connexion/")
def connexion():
    return render_template("connexion.html")

@app.route("/moncompte/")
@login_required
def infocompte():
    return render_template("infoscompte.html")

@app.route("/Apt/")
def aptInfo():
    return render_template("results.html")

@app.route("/upAppt/")
def up_Appt():
    return render_template("chargementappart.html")

