from flask_debugtoolbar import DebugToolbarExtension
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_bcrypt import Bcrypt

db = SQLAlchemy()
debugtoolbar = DebugToolbarExtension()
migrate = Migrate()
login_manager = LoginManager()
bcrypt = Bcrypt()