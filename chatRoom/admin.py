from flask import Flask
from flask_admin import Admin, BaseView, expose
from flask_admin.contrib.sqla import ModelView
from flask_sqlalchemy import SQLAlchemy
from exts import db
from models import User, ChatRecord, ChatConnection
import config

adm = Flask(__name__)
db.init_app(adm)
adm.config.from_object(config)
admin = Admin(adm,name=u'后台管理系统')

db = SQLAlchemy(adm)

@expose('/')
def index(self):
	return self.render('admin/index.html') 

class MyModelViewBase(ModelView):
	column_display_pk = True
	column_display_all_relations = True

class MyModelViewUser(MyModelViewBase):
	column_formatters = dict(
		password = lambda v, c, m, p: '***' + m.password[-2:])
	column_searchable_list = (User.username, )

admin.add_view(MyModelViewUser(User, db.session))
admin.add_view(ModelView(ChatRecord, db.session))

adm.run(debug=True)

