from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from resourse.models.course import Course
from resourse import db

coursebp = Blueprint('course', __name__, url_prefix='/course')


@coursebp.route('/')
def search():
	all_course = Course.query.filter(True).all()
	result = []
	for course in all_course:
		result.append(course.as_dict())
	return jsonify(result)


@coursebp.route('/add', methods=['POST'])
def addcourse():
	new_course = Course(name='UML',description='good course',teacher_id=1, image='https://http.cat/400')
	db.session.add(new_course)
	db.session.commit()

	result = {"code": 200, "flag": True, "message": "secceed"}
	return jsonify(result)
