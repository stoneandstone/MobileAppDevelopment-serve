from resourse import db

class Category(db.Model):
	__tablename__ = 'category'
	id = db.Column(db.String(255), primary_key=True, autoincrement=True)

	def as_dict(self):
		return {c.name: getattr(self, c.name) for c in self.__table__.columns}

	def __repr__(self):
		return '<Category {}>'.format(self.name)
