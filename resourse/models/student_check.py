from resourse import db


class StudentCheck(db.Model):
	__tablename__ = 'student_check'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	check_id = db.Column(db.Integer)
	student_id = db.Column(db.Integer)
	check_time = db.Column(db.DateTime)
	isvalid = db.Column(db.Boolean)

	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}

	def __repr__(self):
		return '<StudentCheck {}>'.format(self.name)
