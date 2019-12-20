from flask import Flask
from SaaS.extensions import debugtoolbar, db, migrate, login_manager, bcrypt

from SaaS.models import Setting

def create_app():

	app = Flask(__name__, instance_relative_config=True)
	app.config.from_object('config')
	app.config.from_pyfile('config.py', silent=True)

	with app.app_context():
		# init extenstions
		init_extensions(app)

		# import views
		from .home.views import main
		from .admin.views import admin

		# register views
		app.register_blueprint(main)
		app.register_blueprint(admin)

	return app


def init_extensions(app):
	debugtoolbar.init_app(app)
	db.init_app(app)
	migrate.init_app(app, db)
	login_manager.init_app(app)
	bcrypt.init_app(app)