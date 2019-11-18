from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from resourse import sqldb

initbp = Blueprint('init', __name__, url_prefix='/api/init')

@initbp.route("")
def init():
	coursesql = "SELECT * FROM course"
	mydb = sqldb.get_db()
	cursor = mydb.cursor()
	cursor.execute(coursesql)
	courses = cursor.fetchall()
	courses_list = []
	for course in courses:
		teaval = (course[2])
		teasql = "SELECT name FROM teacher WHERE idteacher=%d;" % teaval
		cursor.execute(teasql, teaval)
		teacher = cursor.fetchone()[0]
		course_dict = {
			"course_id": course[0],
			"category": course[1],
			"teacher": teacher,
			'name': course[3],
			"numOfStudents": course[4],
			"introduction": course[5]
		}
		courses_list.append(course_dict)

	return jsonify(courses_list)

@initbp.route('/student')
def init_stu():
	idstu = None
	try:
		idstu = int(request.args.get("studentid"))
	except Exception as e:
		print(e)

	if idstu == None:
		return "Bad"
	initsql = "SELECT idcourse FROM favorite WHERE idstudent=%d;" % idstu
	mydb = sqldb.get_db()
	cursor = mydb.cursor()
	cursor.execute(initsql)
	courseids = cursor.fetchall()
	courses_list = []
	print(courseids)
	print("DEBUG-------------------------------DEBUG")
	for courseid in courseids:
		coursesql = "SELECT * FROM course WHERE idcourse=%d;" % courseid[0]
		cursor.execute(coursesql)
		course = cursor.fetchone()

		###
		teaval = (course[2])
		teasql = "SELECT name FROM teacher WHERE idteacher=%d;" % teaval
		cursor.execute(teasql)
		teacher = cursor.fetchone()[0]
		course_dict = {
			"course_id": course[0],
			"category": course[1],
			"teacher": teacher,
			'name': course[3],
			"numOfStudents": course[4],
			"introduction": course[5]
		}
		courses_list.append(course_dict)

	return jsonify(courses_list)
