from flask import Flask
from flask import render_template,request,redirect,url_for,session
from models import User,Question,Answer
from exts import db
from werkzeug.security import generate_password_hash, check_password_hash
from decorators import login_required

import config

app = Flask(__name__)
app.config.from_object(config)
db.init_app(app)


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
        # password = generate_password_hash(password)
        # user = User.query.filter(User.email == email,User.password == password).first()
        # if user:
        user = User.query.filter(User.email == email).first()
        if user:
            user.point = user.point + 5
            if check_password_hash(user.password, password):
                session['user_id']=user.id
                #如果想在31天内都不需要登录
                session.permanent=True
                return redirect(url_for('index'))
            else:
                return u'The password is wrong.'
        else:
            return u'The email is invalid.'

@app.route('/regist/',methods=["GET","POST"])
def regist():
    if request.method=="GET":
        return render_template('regist.html')
    else:
        email = request.form.get('email')
        username = request.form.get('username')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #check whether the email is already registed
        user=User.query.filter(User.email==email).first()
        if user:
            return u'This email is already registed. Please change another one'
        else:
    # check whether two passwords are the same
            if password1!=password2:
                return u'Passwords are not the same.'
            else:
                password=generate_password_hash(password1)
                user=User(email = email, username = username, password = password, number_of_post = 0, number_of_comment = 0, point = 0, grade = 1, friends="???")
                db.session.add(user)
                db.session.commit()
                return redirect(url_for('login'))

@app.route('/question/',methods=['GET','POST'])
@login_required
def question():
    if  request.method == 'GET':
        return render_template('question.html')
    else:
        title = request.form.get('title')
        content = request.form.get('content')
        question = Question(title=title,content=content)
        user_id=session.get('user_id')
        user=User.query.filter(User.id==user_id).first()
        user.number_of_post = user.number_of_post + 1
        user.point = user.point + 20
        question.author =user
        db.session.add(question)
        db.session.commit()
        return redirect(url_for('index'))

@app.route('/detail/<question_id>/')
def detail(question_id):
    question_model = Question.query.filter(Question.id==question_id).first()
    return render_template('detail.html',question=question_model)

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
    answer.author = user
    answer.question = Question.query.filter(Question.id==question_id).first()
    db.session.add(answer)
    db.session.commit()
    return redirect(url_for('detail',question_id=question_id))

@app.route('/logout/',methods=['GET'])
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run()
