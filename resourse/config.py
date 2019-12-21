# -*- coding: utf-8 -*-
class Config():
	SQLALCHEMY_DATABASE_URI = "mysql+mysqlconnector://root:123456@118.25.153.97:3306/Android?charset=utf8"
	SQLALCHEMY_TRACK_MODIFICATIONS = True
	DEBUG = True
	SECRET_KEY = "cl"
	EXPIRES_IN = 21600
