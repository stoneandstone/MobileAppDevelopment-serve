from flask import Blueprint, g, request, session, jsonify, current_app


from resourse.models.check import Check
from resourse.models.student_check import StudentCheck
from resourse.models.student import Student
from resourse.models.take import Take
from resourse.models.course import Course

checkbp = Blueprint('check', __name__, url_prefix='/check')

@checkbp.route('/', methods=['GET'])
def getAllCheck():
	try:
		student_name = g.uid
		student = Student.query.filter(Student.username == student_name).first()
		student_id = student.id

		all_take = Take.query.filter(Take.student_id == student_id).all()
		course_ids = []
		for take in all_take:
			course_id = take.course_id
			course_ids.append(course_id)

		all_check = []
		for course_id in course_ids:
			checks = Check.query.filter(Check.course_id==course_id).all()
			all_check = all_check + checks

		checks_dict = []
		for check in all_check:
			check_dict = check.as_dict()
			student_check = StudentCheck.query.filter(StudentCheck.student_id==student_id and StudentCheck.check_id==check.id).first()
			if student_check is None:
				check_dict['status'] = False
			elif student_check.isvalid is None or student_check == False:
				check_dict['status'] = False
			elif student_check.isvalid:
				check_dict['status'] = True

			course = Course.query.filter(Course.id == check.course_id).first()
			check_dict['course'] = course.as_dict()
			checks_dict.append(check_dict)

		return jsonify(checks_dict)
	except:
		pass
	return jsonify([])
