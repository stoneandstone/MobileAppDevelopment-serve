from resourse import db

class Course(db.Model):
	__tablename__ = 'course'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(255), nullable=False)
	description = db.Column(db.String(255))
	teacher_id = db.Column(db.Integer)
	image = db.Column(db.String(255))

	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}

	def __repr__(self):
		return '<Course {}>'.format(self.name)
