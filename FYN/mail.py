from mailjet_rest import Client
import os
from flask import url_for

def envoyer_mail(mail,username):
    api_key = '4758ff5a850d727d75cbc8e7bf09c958'
    api_secret = '50594a1889d64dee6cbf9d98f5ee5c09'
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
    'Messages': [
        {
        "From": {
            "Email": "rajesw.priya@gmail.com",
            "Name": "FindYourNest"
        },
        "To": [
            {
            "Email": mail,
            "Name": username
            }
        ],
        "Subject": "Inscription",
        "TextPart": "bienvenue",
        "HTMLPart": "<h3>Bonjour, nous vous souhaitons la bienvenue sur notre site. Bonne journée",
        "CustomID": "AppGettingStartedTest"
        }
    ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())


def forget_password(mail, username):
    api_key = '4758ff5a850d727d75cbc8e7bf09c958'
    api_secret = '50594a1889d64dee6cbf9d98f5ee5c09'
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
    'Messages': [
        {
        "From": {
            "Email": "rajesw.priya@gmail.com",
            "Name": "FindYourNest"
        },
        "To": [
            {
            "Email": mail,
            "Name": username
            }
        ],
        "Subject": "Réinitialiser votre mot de passe",
        "TextPart": "Réinitialisation",
        "HTMLPart": """ <b> Réinitialiser votre mot de passe : </b> <br/>
                    Vous nous avez indiqué avoir oublié votre mot de passe.
                    Si c'est vraiment le cas, cliquez sur le lien ci-dessous afin de le réinitialiser: <br/>
                    <a href='http://127.0.0.1:8080/reinitialisation_pwd/'>Réinitialiser le mot de passe</a> <br/>
                    Si vous n'aviez pas l'intention de réinitialiser votre mot de passe, ignorez simplement cet e-mail, et votre mot de passe ne sera pas changé <br/>
                    Merci, en vous souhaitant une bonne journée."""
        }
    ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())