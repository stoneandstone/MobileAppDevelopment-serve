from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from resourse.models.course import Course
from resourse.models.teacher import Teacher
from resourse.models.student import Student
from resourse.models.take import Take
from resourse import db

coursebp = Blueprint('course', __name__, url_prefix='/course')

# 获得所有的课程
@coursebp.route('/')
def search():
	all_course = Course.query.filter(True).all()
	result = []
	for course in all_course:
		obj_dict = course.as_dict()
		teacher = Teacher.query.filter(Teacher.id==course.teacher_id).first()
		obj_dict["teacher_name"] = teacher.name
		result.append(obj_dict)
	return jsonify(result)


@coursebp.route('/take', methods=['GET','POST'])
def addcourse():
	student_name = g.uid
	student = Student.query.filter(Student.username == student_name).first()
	student_id = student.id
	if request.method == 'GET':
		try:
			all_take = Take.query.filter(Take.student_id == student_id).all()
			result = []
			for take in all_take:
				course_id = take.course_id
				course = Course.query.filter(Course.id == course_id).first()
				obj_dict = course.as_dict()
				result.append(obj_dict)

			return jsonify(result)
		except:
			result = "failed"
			return jsonify(result)

	elif request.method == 'POST':
		try:


			take_json = request.get_json()
			course_id = take_json["course_id"]

			# 判断是否已经选上
			otake = Take.query.filter(Take.course_id == course_id and Take.student_id == student_id).first()
			if otake is not None:
				result = {"code": 200, "flag": True, "message": "already added"}
				return jsonify(result)

			ntake = Take(student_id=student_id, course_id=course_id)
			db.session.add(ntake)
			db.session.commit()
			result = {"code": 200, "flag": True, "message": "succeed"}
		except:
			result = {"code": 201, "flag": False, "message": "failed"}
		return jsonify(result)
