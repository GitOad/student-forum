import os

DEBUG=True

SECRET_KEY=os.urandom(24)

DIALECT = 'mysql'
DRIVER = 'mysqldb'
USERNAME = 'root'
PASSWORD = ''
HOST = 'localhost'
PORT = '3306'
DATABASE = 'db_demo1'
SQLALCHEMY_DATABASE_URI = "{}+{}://{}:{}@{}:{}/{}".format(DIALECT,DRIVER,USERNAME,PASSWORD,HOST,PORT,DATABASE)

SQLALCHEMY_TRACK_MODIFICATIONS = False

WHOOSH_BASE='path/to/whoosh/base' 
