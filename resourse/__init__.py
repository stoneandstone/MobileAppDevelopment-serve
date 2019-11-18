from flask import Flask
from resourse.api import course, video, auth, init


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY='dev'
    )

    app.config.from_pyfile("app.cfg")

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    @app.route('/')
    def initapp():
        return "Init"


    app.register_blueprint(auth.authbp)
    app.register_blueprint(video.filebp)
    app.register_blueprint(course.coursebp)
    app.register_blueprint(init.initbp)

    return app
