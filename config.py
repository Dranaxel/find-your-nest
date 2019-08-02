#This file contains all the fixed config variables

class Config(object):
    Debug = False #Allow using debugging features
    SECRET_KEY = b"ZLtx0B9Lnsoq32oV_lXG/S[c1}g_vl"

class DevelopmentConfig(object):
    Debug = True
    SECRET_KEY = b'This is a huge secret'
