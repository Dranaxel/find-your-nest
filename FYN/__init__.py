#init modules

from flask import Flask
from flask_login import LoginManager
import sqlite3

app = Flask(__name__)
app.config.from_object('config.Config')
#app.config['upload_pro'] = upload_pro

login_manager = LoginManager()
login_manager.init_app(app)

import FYN.views
