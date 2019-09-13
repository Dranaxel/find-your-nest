from mailjet_rest import Client
import os

def envoyer_mail(mail,username):
    api_key = '4758ff5a850d727d75cbc8e7bf09c958'
    api_secret = '50594a1889d64dee6cbf9d98f5ee5c09'
    mailjet = Client(auth=(api_key, api_secret), version='v3.1')
    data = {
    'Messages': [
        {
        "From": {
            "Email": "rajesw.priya@gmail.com",
            "Name": "Priya"
        },
        "To": [
            {
            "Email": mail,
            "Name": username
            }
        ],
        "Subject": "Inscription FINDYOURNEST",
        "TextPart": "bienvenue",
        "HTMLPart": "<h3>Bonjour, nous vous souhaitons la bienvenue sur notre site. Bonne journée",
        "CustomID": "AppGettingStartedTest"
        }
    ]
    }
    result = mailjet.send.create(data=data)
    print(result.status_code)
    print(result.json())
