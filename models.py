from exts import db
from datetime import datetime
from datetime import date
from jieba.analyse.analyzer import ChineseAnalyzer
import flask_whooshalchemyplus

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
    register_time = db.Column(db.DateTime, default = datetime.now)
    last_login_time = db.Column(db.DateTime)
    introduction = db.Column(db.Text)

    photo = db.Column(db.String(100), nullable=True)  # 存储图片的路径
    confirmed = db.Column(db.Boolean, nullable=False, default=False)#新！！
    confirmed_on = db.Column(db.DateTime, nullable=True)#新！！

class Question(db.Model):
    __tablename__ = 'question'
    __searchable__ = ['content', 'title']
    __analyzer__ = ChineseAnalyzer()
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    title = db.Column(db.String(100), nullable = False)
    content = db.Column(db.Text, nullable = False)
    # type = db.Column(db.Text, nullable = False) #帖子的分类
    create_time = db.Column(db.DateTime, default = datetime.now)
    author_id = db.Column(db.Integer,db.ForeignKey('user.id'))

    comments = db.relationship('Answer', backref='question', lazy='dynamic', cascade='all, delete-orphan', passive_deletes=True)
    # author = db.relationship('User',backref = db.backref('questions'))

    def __repr__(self):
        return '{0}(title={1})'.format(self.__class__.__name__, self.title)


class Answer(db.Model):
    __tablename__ = 'answer'
    id = db.Column(db.Integer, primary_key = True, autoincrement = True)
    content = db.Column(db.Text, nullable = False)
    # total_reported_time = db.Column(db.Integer)  #被举报的总数
    question_id = db.Column(db.Integer, db.ForeignKey('question.id', ondelete='CASCADE'))
    author_id = db.Column(db.Integer)
    create_time = db.Column(db.DateTime, default = datetime.now)

    question = db.relationship('Question',backref = db.backref('answers',order_by = id.desc()))
    # author = db.relationship('User',backref = db.backref('answers'))

class Information(db.Model):
    __tablename__ = 'info'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)

    gender = db.Column(db.String(100))
    birthday = db.Column(db.String(100))
    age = db.Column(db.Integer)
    major = db.Column(db.String(100))
    group = db.Column(db.String(100)) #i.e. class
    hobbies = db.Column(db.Text)

    number_of_followed = db.Column(db.Integer) #粉丝总数
    number_of_following = db.Column(db.Integer) #关注总数

    user_id = db.Column(db.Integer, db.ForeignKey('user.id')) #foreign key (connect to the table "user")

    owner = db.relationship('User',backref = db.backref('information'))

class Following(db.Model):
    __tablename__ = 'follow'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    user_id = db.Column(db.Integer)
    followed_user_id = db.Column(db.Integer)
