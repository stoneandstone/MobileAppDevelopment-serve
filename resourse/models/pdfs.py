from resourse import db

class PDF(db.Model):
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	course_id = db.Column(db.Integer)
	file_name = db.Column(db.String(255), nullable=False)

	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}

	def __repr__(self):
		return '<PDF {}>'.format(self.name)
