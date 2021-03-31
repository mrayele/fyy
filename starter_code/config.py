import os

# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

class Config(object):
	DEBUG = True # Enable debug mode.
	SECRET_KEY = os.urandom(32)
	SQLALCHEMY_DATABASE_URI = 'postgresql://postgres@localhost:5432/fyyur'
	SQLALCHEMY_TRACK_MODIFICATIONS = False