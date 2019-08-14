#This file contains all the fixed config variables

class Config(object):
	DEBUG = False #Allow using debugging features
	SECRET_KEY = b"ZLtx0B9Lnsoq32oV_lXG/S[c1}g_vl"
	NAVITIA = "6451613e-bdfe-4194-a3b5-91164c6ae89f"

class DevelopmentConfig(Config):
    Debug = True
    SECRET_KEY = b'This is a huge secret'
