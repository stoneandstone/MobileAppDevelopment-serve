from flask import Flask, g, current_app
from flask_sqlalchemy import SQLAlchemy


from . import config

app = Flask(__name__)
db = SQLAlchemy()

def create_app():
	app.config.from_object(config.Config)
	db.init_app(app)
	with app.app_context():
		# Imports
		from resourse.api import courseBp, fileBp, authBp, checkBp
		app.register_blueprint(courseBp.coursebp)
		app.register_blueprint(authBp.authbp)
		app.register_blueprint(fileBp.filebp)
		app.register_blueprint(checkBp.checkbp)
		# Create tables for our models
		db.create_all()
		return app
