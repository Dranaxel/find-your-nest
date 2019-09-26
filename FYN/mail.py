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
        "TextPart": "Bienvenue",
        "HTMLPart": """<center><h2>Bienvenue</h2><br/>
                    Bonjour """+ username +""",<br/> 
                    Nous vous souhaitons la bienvenue sur notre site FindYourNest. 
                    Vous pouvez maintenant accéder aux diverses fonctionnalités proposé par notre plateforme entièrement gratuite.<br/>
                    Nous vous donnons donc rendez-vous sur notre site en suivant le lien suivant : <br/>
                    <a href="https://find-your-nest-ywhzbcfbpq-ew.a.run.app/">Commencer</a>
                    </center>"""
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
        "HTMLPart": """<FONT color="black"><center><h2>Réinitialiser votre mot de passe : </h2><br/>
                    <FONT size="4">Vous nous avez indiqué avoir oublié votre mot de passe.
                    Si c'est vraiment le cas, cliquez sur le lien ci-dessous afin de le réinitialiser: <br/>
                    <a href="https://find-your-nest-ywhzbcfbpq-ew.a.run.app/reinitialisation_pwd">Réinitialiser le mot de passe</a> <br/>
                    Si vous n'aviez pas l'intention de réinitialiser votre mot de passe, ignorez simplement cet e-mail, et votre mot de passe ne sera pas changé </FONT><br/>
                    <FONT size="2"> Le lien suivant ne fonctionne pas ? Copiez l'adresse suivante dans votre navigateur: <br/>
                    https://find-your-nest-ywhzbcfbpq-ew.a.run.app/reinitialisation_pwd/</FONT></center></FONT>"""
        }
    ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())


def contact_mail(username1, email1, phone, msg, email2, username2, bien):
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
            "Email": email2,
            "Name": username2
            }
        ],
        "Subject": "Demande de contact",
        "TextPart": "Demande de contact",
        "HTMLPart": """<center><h2>Demande de contact : </h2><br/>
                    Un utilisateur semble fortement intéressé par votre bien et il souhaiterait échanger avec vous. 
                    De ce fait, vous trouverez ci-dessous les informations nécessaires pour le recontacter ultérieurement : <br/>
                    <b> Prénom : </b>""" + username1 + 
                    """ <br/>
                    <b> Adresse email : </b>""" + email1 +
                    """ <br/>
                    <b> Numéro de téléphone : </b>""" + phone + 
                    """<br/>
                    <b> Message : </b>""" + msg +
                    """<br/>
                    <b> Bien : </b>""" + bien + """</center>"""
        }
    ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())