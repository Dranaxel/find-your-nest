#This file contains all the fixed config variables

class Config(object):
    DEBUG = False #Allow using debugging features
    SECRET_KEY = b"ZLtx0B9Lnsoq32oV_lXG/S[c1}g_vl"
    NAVITIA_KEY = "6451613e-bdfe-4194-a3b5-91164c6ae89f"
    NAVITIA_URL = "http://api.navitia.io/v1/journeys"
    OPENCAGE_KEY = "31dbec8c7f4844a6aafa18c738aea931"

class DevelopmentConfig(Config):
    DEBUG = False
    SECRET_KEY = b'This is a huge secret'
