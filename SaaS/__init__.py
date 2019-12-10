from flask import Flask

def create_app():

	app = Flask(__name__, instance_relative_config=True)
	app.config.from_object('config')
	app.config.from_pyfile('config.py', silent=True)

	with app.app_context():
		# import views
		from .home.views import main

		# register views
		app.register_blueprint(main)

	return app

