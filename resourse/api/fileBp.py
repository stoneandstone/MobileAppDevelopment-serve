import os

from flask import Blueprint, request, flash, Response, jsonify, send_from_directory, g
from werkzeug.utils import secure_filename

from resourse.models.course import Course
from resourse.models.take import Take
from resourse.models.student import Student
from resourse.models.pdfs import PDF
from resourse import db

filebp = Blueprint('file', __name__, url_prefix='/file')

JPEG_PATH = '/root/Android/file/jpeg/'
PDF_PATH = '/root/Android/file/pdf/'


@filebp.route('/jpeg/<picture_name>', methods=('GET', 'POST'))
def picture(picture_name):
	file_exist = os.path.exists(JPEG_PATH + picture_name)
	if request.method == 'GET':
		if not file_exist:
			return "No Such pic"
		try:
			response = Response(JPEG_PATH + picture_name, mimetype="image/jpeg")
			return send_from_directory(JPEG_PATH, picture_name)
		except Exception as e:
			return jsonify({"code": "unexception", "message": "{}".format(e)})

		return "JPEG GET"
	elif request.method == 'POST':
		if 'file' not in request.files:
			print(dict(request.files))
			return "No Picture POST"
		file = request.files['file']
		if file.filename == '':
			flash('No selected file')
			return 'No selected file'
		else:
			filename = secure_filename(file.filename)
			file.save(JPEG_PATH + filename)
			return "Picture Get %s" % picture_name


@filebp.route('/pdf', methods=('GET', 'POST'))
def pdf():
	pdf_json = request.get_json()
	if request.method == "GET":
		student_name = g.uid
		student = Student.query.filter(Student.username == student_name).first()
		student_id = student.id

		all_take = Take.query.filter(Take.student_id == student_id).all()
		result = []
		for take in all_take:
			course_id = take.course_id
			course = Course.query.filter(Course.id == course_id).first()
			obj_dict = course.as_dict()
			course_pdfs = PDF.query.filter(PDF.course_id == course_id).all()
			pdfs_dict = [p.as_dict() for p in course_pdfs]
			obj_dict['pdfs'] = pdfs_dict
			result.append(obj_dict)

		return jsonify(result)
	return jsonify("haha")


@filebp.route('/pdf/<course_id>/<file_name>', methods=('GET', 'POST'))
def getPDF(course_id, file_name):
	if request.method == "GET":
		pdf_path = PDF_PATH + '/' + course_id + '/'
		file_exist = os.path.exists(pdf_path + file_name)
		if not file_exist:
			return "no such pdf"
		try:
			response = Response(JPEG_PATH + pdf_path, mimetype="application/pdf")
			return send_from_directory(pdf_path, file_name)
		except Exception as e:
			return jsonify({"code": "unexception", "message": "{}".format(e)})
