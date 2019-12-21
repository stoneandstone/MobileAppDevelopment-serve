from resourse import db


class Teacher(db.Model):
	__tablename__ = 'teacher'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	name = db.Column(db.String(255), nullable=True)
	password = db.Column(db.String(255), nullable=True)
	e_mail = db.Column(db.String(255))
	create_time = db.Column(db.DateTime)

	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}

	def __repr__(self):
		return '<Teacher {}>'.format(self.name)
