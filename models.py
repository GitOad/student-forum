from exts import db
from datetime import datetime
from datetime import date

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer,primary_key = True, autoincrement = True)
    email = db.Column(db.String(100), nullable = False, unique = True)
    username = db.Column(db.String(100), nullable = False)
    password = db.Column(db.String(100), nullable = False)

    number_of_post = db.Column(db.Integer)
    number_of_comment = db.Column(db.Integer)
    point = db.Column(db.Integer)
    grade = db.Column(db.Integer)
    friends = db.Column(db.Text, nullable=False)
    register_time = db.Column(db.DateTime, default = datetime.now)
    last_login_time = db.Column(db.DateTime)

class Question(db.Model):
    __tablename__ = 'question'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    create_time = db.Column(db.DateTime, default = datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    author = db.relationship('User',backref = db.backref('questions'))

class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    content = db.Column(db.Text, nullable = False)
    question_id = db.Column(db.Integer, db.ForeignKey('question.id'))
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    create_time = db.Column(db.DateTime, default = datetime.now)

    question = db.relationship('Question',backref = db.backref('answers',order_by = id.desc()))
    author = db.relationship('User',backref = db.backref('answers'))

class Information(db.Model):
    __tablename__ = 'info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    gender = db.Column(db.String(100), nullable = False)
    birthday = db.Column(db.String(100), nullable = False)
    age = db.Column(db.Integer)
    major = db.Column(db.String(100), nullable = False)
    group = db.Column(db.String(100), nullable = False) #i.e. class
    hobbies = db.Column(db.Text, nullable = False)
    introduction = db.Column(db.Text, nullable=False)

    #photo = db.Column(db.LargeBinary(length=2048))  # 以二进制形式存储图片
    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #foreign key (connect to the table "user")

    owner = db.relationship('User',backref = db.backref('information'))
