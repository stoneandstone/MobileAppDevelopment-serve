import functools

from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from resourse import sqldb

authbp = Blueprint('auth', __name__, url_prefix='/api/auth')


@authbp.route('/register', methods=('GET', 'POST'))
def register():
	if request.method == 'POST':
		register_info = request.get_json()
		regist_type = register_info['type']
		regist_id = register_info['id']
		username = register_info['username']
		password = register_info['password']
		email = register_info['email']

		sql = "INSERT INTO student (idstudent, name, password, email) VALUES (%s, %s, %s, %s);" \
			if regist_type == 'student' else \
			"INSERT INTO teacher(idstudent, name, password, email) VALUES (%s, %s, %s, %s);"
		val = (regist_id, username, password, email)
		mydb = sqldb.get_db()
		cursor = mydb.cursor()
		cursor.execute(sql, val)
		mydb.commit()
		mydb.disconnect()
		return "Post Regist info username: %s password %s" % (username, password)
	else:
		return "Get Regist info"


@authbp.route('/login', methods=('GET', 'POST'))
def login():
	if request.method == 'GET':
		print('Login GET')
		return 'Login GET'
	else:
		print('Login POST')

		# login_info = request.get_json()
		# type = login_info['type']
		# login_id = login_info['id']
		# login_passwd = login_info['password']
		login_info = dict(request.form)
		type = login_info['type']
		login_id = login_info['id']
		login_passwd = login_info['password']
		sql = "SELECT * FROM student WHERE idstudent = %s;" if type == 'student' \
			else "SELECT * FROM teacher WHERE idteacher = %s;"
		val = (login_id,)
		mydb = sqldb.get_db()
		cursor = mydb.cursor()
		cursor.execute(sql, val)
		result = cursor.fetchone()
		if result == None:
			return "No such id in " + type
		result = list(tuple(result))
		if result[2] == login_passwd:
			print("Login Succeed")
			session.clear()
			session["type"] = type
			session["id"] = login_id
			return "Login Succeed"
		else:
			return "Password Error"


@authbp.before_app_request
def load_logged_in_user():
	user_id = session.get('user_id')
	if user_id is None:
		g.user = None
	else:
		g.user = user_id
