from resourse import db
import datetime

class Check(db.Model):
	__tablename__ = 'check'
	id = db.Column(db.Integer, primary_key=True, autoincrement=True)
	course_id = db.Column(db.Integer)
	create_time = db.Column(db.Integer, default=1577049460)

	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}

	def __repr__(self):
		return '<Check {}>'.format(self.name)
