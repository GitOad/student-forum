from exts import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key = True, autoincrement = True)
    username = db.Column(db.String(100), nullable = False)
    password = db.Column(db.String(100), nullable = False)

class ChatRecord(db.Model):
    __tablename__ = 'chatrecord'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    content = db.Column(db.Text, nullable = False)
    create_time = db.Column(db.DateTime, default = datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))
    chat_id = db.Column(db.Integer,db.ForeignKey('chatconnection.id'))
    # author = db.relationship('User',backref = db.backref('chatrecord'))

class ChatConnection(db.Model):
    __tablename__ = 'chatconnection'
    id = db.Column(db.Integer,primary_key = True, autoincrement = True)
    u_id1 = db.Column(db.Integer)
    u_id2 = db.Column(db.Integer)