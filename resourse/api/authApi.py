from flask import Blueprint, g, request, session, jsonify, current_app
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer, SignatureExpired
import datetime
import hashlib

from resourse import app, db
from resourse.models.student import Student
from resourse.models.teacher import Teacher

authbp = Blueprint('auth', __name__, url_prefix='/auth')


@app.route('/test', methods=['GET'])
def test():
	result = {'code': 200, 'message': 'test'}

	return jsonify(result)


def verify_token(token):
	# 参数为私有秘钥，跟上面方法的秘钥保持一致
	s = Serializer(current_app.config["SECRET_KEY"])
	try:
		# 转换为字典
		data = s.loads(token)
	except BaseException:
		return "登录未授权"
	except SignatureExpired:
		return "登录已过期"
	uid = data["id"]
	login_type = data["type"]
	return uid, login_type


def md5(password):
	md5 = hashlib.md5()
	md5.update(password.encode())
	return md5.hexdigest()


def create_token(id, type):
	s = Serializer(current_app.config["SECRET_KEY"], expires_in=current_app.config["EXPIRES_IN"])
	# 接收用户id转换与编码
	token = s.dumps({'id': id, 'type': type}).decode("ascii")
	return token


@app.before_request
def is_login():
	if request.path == "/auth/login" or request.path == "/auth/register" or request.path == '/test':
		return None
	token = request.headers.get("Authorization")
	if token:
		uid, login_type = verify_token(token)
		if type(uid) is str:
			g.uid = uid
			g.type = login_type
		else:
			return jsonify(code=20002, flag=False, message=uid)
	else:
		return jsonify(code=20001, flag=False, message="请先登录")


@authbp.route('/register', methods=('GET', 'POST'))
def register():
	if request.method == 'POST':
		register_info = request.get_json()
		regist_type = register_info['type']
		username = register_info['username']
		password = register_info['password']
		email = register_info['email']

		if regist_type == 'student':
			try:
				student = Student.query.filter(Student.username == username).all()
				if student[0]:
					result = {'code': '201', 'flag': False, 'message': '账号已存在'}
					return jsonify(result)
			except Exception as e:
				print(e)
			student = Student(username=username, password=md5(password), e_mail=email,
							  create_time=datetime.datetime.now())
			try:
				db.session.add(student)
				db.session.commit()
				db.session.flush()
				print(student.as_dict())
				result = {'code': '200', 'flag': True, 'message': '注册成功'}
				return jsonify(result)
			except Exception as e:
				result = {'code': '201', 'flag': False, 'message': e}
				return jsonify(result)

		elif regist_type == 'teacher':
			try:
				teacher = Teacher.query.filter(Teacher.username == username).all()
				if teacher[0]:
					result = {'code': '201', 'flag': False, 'message': '账号已存在'}
					return jsonify(result)
			except Exception as e:
				pass
			teacher = Teacher(name=username, password=md5(password), e_mail=email,
							  create_time=datetime.datetime.now())
			try:
				db.session.add(teacher)
				db.session.commit()
				db.session.flush()
				print(teacher.as_dict())
				result = {'code': '200', 'flag': True, 'message': '注册成功'}
				return jsonify(result)
			except Exception as e:
				result = {'code': '201', 'flag': False, 'message': '错误'}
				return jsonify(result)

		result = {'code': '201', 'flag': False, 'message': '无法识别'}
		return jsonify(result)
	else:
		return "Get Regist info"


@authbp.route('/login', methods=('GET', 'POST'))
def login():
	if request.method == 'GET':
		print('Login GET')
		return 'Login GET'
	else:
		print('Login POST')

		login_info = request.get_json()
		type = login_info['type']
		login_username = login_info['username']
		login_password = login_info['password']

		if type == 'student':
			try:
				student = Student.query.filter(Student.username == login_username).first()
				if student is not None:
					username = student.username
					password = student.password
					if md5(login_password) == password:
						token = create_token(username, 'student')
						result = {'code': '200', 'flag': True, 'token': token, 'message': '登录成功'}
						return jsonify(result)
					else:
						result = {'code': '201', 'flag': False, 'message': '密码错误'}
						return jsonify(result)

				else:
					result = {'code': '201', 'flag': False, 'message': '不存在该用户'}
					return jsonify(result)
			except:
				result = {'code': '500', 'flag': False, 'message': '错误'}
				return jsonify(result)

		elif type == 'teacher':
			try:
				teacher = Teacher.query.filter(Teacher.name == login_username).first()
				if teacher is not None:
					username = teacher.name
					password = teacher.password
					if md5(login_password) == password:
						token = create_token(username, 'teacher')
						result = {'code': '200', 'flag': True, 'token': token, 'message': '登录成功'}
						return jsonify(result)
					else:
						result = {'code': '201', 'flag': False, 'message': '密码错误'}
						return jsonify(result)

				else:
					result = {'code': '201', 'flag': False, 'message': '不存在该用户'}
					return jsonify(result)
			except:
				result = {'code': '500', 'flag': False, 'message': '错误'}
				return jsonify(result)

		result = {'code': '201', 'flag': False, 'message': '无法识别'}
		return jsonify(result)
