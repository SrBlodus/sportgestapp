#config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'mysql://aabr:031297.Ale@192.168.3.15/sportgest' #192.168.3.15
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24).hex()
