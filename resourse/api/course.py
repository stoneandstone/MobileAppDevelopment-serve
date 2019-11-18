from flask import (
	Blueprint, flash, g, redirect, render_template, request, session, url_for, jsonify
)
from resourse import sqldb

coursebp = Blueprint('course', __name__, url_prefix='/api/course')

COURSE_COLUMN = ['idcourse', 'category', 'idteacher', 'name', 'stunum', 'introduction']


@coursebp.route('/')
def search():
	search_dict = {}
	rkeys = list(request.args.keys())
	for rkey in rkeys:
		if rkey not in COURSE_COLUMN:
			return jsonify({"result": "Bad Args"})
		rvalue = request.args.get(rkey)
		if not rkey and not rvalue:
			search_dict[rkey] = rvalue

	sql = "SELECT * FROM course;"
	val = []
	if len(rkeys):
		sql = sql[:-1] + ' WHERE '
		for rkey in rkeys:
			condiction = rkey + '=%s AND '
			sql = sql + condiction
			rval = request.args.get(rkey)
			val.append(rval)
		sql = sql[:-5] + ";"
	val = tuple(val)

	mydb = sqldb.get_db()
	cursor = mydb.cursor()
	cursor.execute(sql, val)
	course_results = cursor.fetchall()
	courses_list = []
	for course in course_results:
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
			"introduction" : course[5]
		}
		courses_list.append(course_dict)

	return jsonify(courses_list)
