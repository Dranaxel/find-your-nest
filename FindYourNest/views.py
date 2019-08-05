from FindYourNest import app, login_manager
from flask import render_template

#laoding the login manager
@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)

@app.route("/")
def main():
    return render_template('index.html')

@app.route("/connexion/")
def connexion():
    return render_template("connexion.html")
