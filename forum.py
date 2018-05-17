from flask import Flask,abort
from flask import render_template,request,redirect,url_for,session
from models import User,Question,Answer,Information,Following
from exts import db
from werkzeug.security import generate_password_hash, check_password_hash
from decorators import login_required
from datetime import datetime
from sqlalchemy import or_
import flask_whooshalchemyplus
from flask_whooshalchemyplus import index_all
from flask_uploads import UploadSet, IMAGES, configure_uploads, ALL

import config,os

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)
flask_whooshalchemyplus.init_app(app)

app.config['UPLOADED_PHOTO_DEST'] = '/static/images'
app.config['UPLOADED_PHOTO_ALLOW'] = IMAGES

photos = UploadSet('PHOTO')
configure_uploads(app, photos)

@app.route('/')
def index():
    context = {
        'questions': Question.query.order_by('-create_time').all()
    }
    if session.get('user_id'):
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        return render_template('index.html',user = user, **context)
    else:
        return render_template('index.html',**context)

@app.route('/login/',methods=["GET","POST"])
def login():
    if request.method=="GET":
        return render_template('login.html')
    else:
        email = request.form.get('email')
        password = request.form.get('password')
        user = User.query.filter(User.email == email).first()

        if user:
            if check_password_hash(user.password, password):
                user.point = user.point + 5

                if user.point >= 50 and user.point < 100:
                    user.grade = 2
                elif user.point >= 100 and user.point < 200:
                    user.grade = 3
                elif user.point >= 200 and user.point < 500:
                    user.grade = 4
                else:
                    user.grade = 5

                session['user_id']=user.id
                session['login_time'] = user.last_login_time
                user.last_login_time = datetime.now()
                #如果想在31天内都不需要登录
                session.permanent=True
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('index'))
            else:
                return u'The password is wrong.'
        else:
            return u'The email is invalid.'

@app.route('/register/',methods=["GET","POST"])
def register():
    if request.method=="GET":
        return render_template('register.html')
    else:
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')
        #check whether the email is already registered
        user = User.query.filter(User.email==email).first()

        if user:
            return u'This email is already registered. Please change another one'
        else:
    # check whether two passwords are the same
            if password1!=password2:
                return u'Passwords are not the same.'
            else:
                password=generate_password_hash(password1)
                user=User(email = email, username = username, password = password, number_of_post = 0, number_of_comment = 0, point = 0, grade = 1, photo = "!!!")

                info = Information(user_id = user.id)
                info.owner = user
                db.session.add(user)
                db.session.add(info)
                db.session.commit()
                return redirect(url_for('login'))

@app.route('/question/',methods=['GET','POST'])
@login_required
def question():
    if request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title,content=content)
        user_id=session.get('user_id')
        user=User.query.filter(User.id==user_id).first()

        user.number_of_post = user.number_of_post + 1
        user.point = user.point + 20

        if user.point >= 50 and user.point < 100:
            user.grade = 2
        elif user.point >= 100 and user.point < 200:
            user.grade = 3
        elif user.point >= 200 and user.point < 500:
            user.grade = 4
        else:
            user.grade = 5

        question.author = user
        flask_whooshalchemyplus.index_one_model(Question)
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/detail/<question_id>/')
def detail(question_id):
    question_model = Question.query.filter(Question.id==question_id).first()
    if session.get('user_id'):
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        return render_template('detail.html', user=user, question=question_model)
    else:
        return render_template('detail.html', question=question_model)

@app.route('/add_answer/',methods=['POST'])
@login_required
def add_answer():
    question_id = request.form.get('question_id')
    content = request.form.get('answer_content')
    answer = Answer(content=content)
    user_id = session.get('user_id')
    user = User.query.filter(User.id == user_id).first()

    user.number_of_comment = user.number_of_comment + 1
    user.point = user.point + 10

    if user.point >= 50 and user.point < 100:
        user.grade = 2
    elif user.point >= 100 and user.point < 200:
        user.grade = 3
    elif user.point >= 200 and user.point < 500:
        user.grade = 4
    else:
        user.grade = 5

    answer.author = user
    answer.question = Question.query.filter(Question.id==question_id).first()
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail',question_id=question_id))

@app.route('/logout/',methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/edit/', methods=['GET','POST'])
@login_required
def edit():
    if request.method == 'GET':
        return render_template('edit_personal_detail.html')
    else:
        if 'photo' in request.files: #如果用户上传了头像
            filename = photos.save(request.files['photo'])
            url = photos.url(filename)

            username = request.form.get('username')
            birthday = request.form.get('birthday')
            gender = request.form.get('gender')
            age = request.form.get('age')
            major = request.form.get('major')
            group = request.form.get('group')  # group 代表class
            hobbies = request.form.get('hobbies')
            introduction = request.form.get('introduction')
        else:
            url = "!!!"
            username = request.form.get('username')
            birthday = request.form.get('birthday')
            gender = request.form.get('gender')
            age = request.form.get('age')
            major = request.form.get('major')
            group = request.form.get('group')#group 代表class
            hobbies = request.form.get('hobbies')
            introduction = request.form.get('introduction')



        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        user.username = username
        user.photo = url
        user.introduction = introduction

        information = Information.query.filter(Information.user_id == user_id).first()
        information.birthday = birthday
        information.gender = gender
        information.age = age
        information.major = major
        information.group = group
        information.hobbies = hobbies



        information.owner = user
        db.session.add(information)
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('info', user_id=user_id))


@app.route('/info/<user_id>/')
@login_required
def info(user_id):
    user_model = User.query.filter(User.id == user_id).first()
    info_model = Information.query.filter(Information.user_id == user_id).first()

    info_model.number_of_following = Following.query.filter(Following.user_id == user_id).count()
    info_model.number_of_followed = Following.query.filter(Following.followed_user_id == user_id).count()

    questions = {
        'questions': Question.query.filter(Question.author_id == user_id).all()
    }
    # questions = {
    #     'questions': Question.query.filter(Question.author_id == user_id).all()
    # }
    # f = Following.query.filter(Following.user_id == user_id).all()

    # user_model.friends = f[1].followed_user_id


    return render_template('default_personal_detail.html', **questions,user=user_model,info=info_model,time=session.get('login_time'))

@app.route('/search', methods=['POST','GET'])
def search():
    search=request.form.get('q')
    if not search:
        return redirect(url_for('index'))
    return redirect(url_for('search_results', query=search))


@app.route('/search_results/<query>')
def search_results(query):
    results = Question.query.whoosh_search(query).all()

    if session.get('user_id'):
        user_id = session.get('user_id')
        user = User.query.filter(User.id == user_id).first()
        return render_template('search_results.html', user=user, query=query, results=results)
    else:
        return render_template('search_results.html', query=query, results=results)


if __name__ == '__main__':
    app.run()
