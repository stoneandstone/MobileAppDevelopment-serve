import os

from flask import Blueprint, request, flash, Response, jsonify, send_from_directory
from resourse import sqldb
from werkzeug.utils import secure_filename

filebp = Blueprint('file', __name__, url_prefix='/api/file')

JPG_PATH = '/root/Android/file/jpg/'


@filebp.route('/jpg/<picture_name>', methods=('GET', 'POST'))
def picture(picture_name):
	file_exist = os.path.exists(JPG_PATH + picture_name)
	if request.method == 'GET':
		if not file_exist:
			return "No Such Picture"
		try:
			response = Response(JPG_PATH + picture_name, mimetype="image/jpeg")
			return send_from_directory(JPG_PATH, picture_name)
		except Exception as e:
			return jsonify({"code": "unexception", "message": "{}".format(e)})

		return "JPG GET"
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
			file.save(JPG_PATH + filename)
			return "Picture Get %s" % picture_name
