from resourse import db

class Student(db.Model):
	__tablename__ = 'student'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	username = db.Column(db.String(255), nullable=False, unique=True)
	password = db.Column(db.String(255), nullable=False)
	e_mail = db.Column(db.String(255))
	create_time = db.Column(db.DateTime)

	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}

	def __repr__(self):
		return '<Student {}>'.format(self.name)
