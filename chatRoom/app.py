from flask import Flask, render_template
from flask_socketio import SocketIO, emit, send, disconnect, join_room, leave_room, rooms
from exts import db
from models import User, ChatRecord, ChatConnection
import config

app = Flask(__name__)
db.init_app(app)
app.config.from_object(config)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

myID = 1
myName = 'Erick'
myPss = '123'
uid = 2

@app.route('/')
def index():
	return render_template('index.html')

def selectConnection(id1, id2):
	connection1 = ChatConnection.query.filter(ChatConnection.u_id1==id1, ChatConnection.u_id2==id2)
	connection2 = ChatConnection.query.filter(ChatConnection.u_id1==id2, ChatConnection.u_id2==id1)
	if connection1.one_or_none() == None and connection2.one_or_none() == None:
		return None
	else:
		if connection1.one_or_none() == None:
			return connection2
		else:
			return connection1

# collect data from client
@socketio.on('my event', namespace = '/test')
def test_message(message):
	content = message['data']
	if content != "I'm connected!" and r != "Connected!":
		connection = selectConnection(myID, uid)
		# if connection == None:
		# 	create_connect = ChatConnection(u_id1 = myID, u_id2 = uid)
		# 	db.session.add(create_connect)
		# 	db.session.commit()
		connectionid = connection.first().id
		record = ChatRecord(content = content, author_id = myID, chat_id = connectionid)
		db.session.add(record)
		db.session.commit()
	emit('my response', {'data': message['data']})


# show status and chatting history
@socketio.on('connect', namespace = '/test')
def test_connect():
	emit('my response', {'data': '(system):Connected!'})

	connection = selectConnection(myID, uid)
	if connection == None:
		create_connect = ChatConnection(u_id1 = myID, u_id2 = uid)
		db.session.add(create_connect)
		db.session.commit()
	else:
		connectionid = connection.first().id

		records = ChatRecord.query.filter(ChatRecord.chat_id==connectionid).all()
		#print(records)
		
		for r in records:
			if r.author_id == myID:
				t = r.create_time
				r = r.content
				if r != "I'm connected!" and r != "Connected!":
					emit('my response', {'data': '(historyI ' + str(t) + ')'+ str(r)})	
			else:
				r = r.content
				if r != "I'm connected!" and r != "Connected!":
					emit('her response', {'data': '(historyHer ' + str(t) + ')' + str(r)})	


# connect to another exact client
@socketio.on('join', namespace='/test')
def join(message):
	#uid = message['room']
	connection = selectConnection(myID, uid)
	if connection == None:
		create_connect = ChatConnection(u_id1 = myID, u_id2 = uid)
		db.session.add(create_connect)
		db.session.commit()
	connectionid = selectConnection(myID, uid).first().id
	join_room(connectionid)
	emit('my response', {'data': 'In room: ' + str(connectionid)})


@socketio.on('my_room_event', namespace='/test')
def send_room_message(message):	
	connection = selectConnection(myID, uid)
	connectionid = selectConnection(myID, uid).first().id
	content = message['data']
	connection = selectConnection(myID, uid)
	record = ChatRecord(content = content, author_id = myID, chat_id = connectionid)
	db.session.add(record)
	db.session.commit()
	emit('my response', {'data': message['data']}, room=connectionid)


@socketio.on('leave', namespace='/test')
def leave(message):
	#uid = message['room']
	connectionid = selectConnection(myID, uid).first().id
	leave_room(connectionid)
	emit('my response', {'data': 'Out room: ' + str(connectionid)})


# close socket connection
@socketio.on('disconnect_request', namespace = '/test')
def test_disconnect():
	emit('my response', {'data': '(system)Disconnected!'})
	disconnect()

@socketio.on('disconnect', namespace='/test')
def test_disconnect():
    print('Client disconnected')

if __name__ == '__main__':
	socketio.run(app)
