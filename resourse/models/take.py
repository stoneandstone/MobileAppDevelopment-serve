from resourse import db

class Take(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	student_id = db.Column(db.Integer)
	course_id = db.Column(db.Integer)


	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}

	def __repr__(self):
		return '<Take {}>'.format(self.name)
