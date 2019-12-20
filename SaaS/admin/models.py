import secrets

from datetime import datetime
from flask_login import UserMixin
from ..extensions import db, login_manager, bcrypt


@login_manager.user_loader
def load_user(uid):
	return User.query.get(int(uid))


class User(db.Model, UserMixin):
	__tablename__ = 'users'

	id			= db.Column(db.Integer, primary_key=True)
	username 	= db.Column(db.String(32), nullable=False)
	email 		= db.Column(db.String(64), unique=True, nullable=False)
	password	= db.Column(db.String(128), nullable=False)
	token		= db.Column(db.String(64), unique=True, nullable=False)
	status_id	= db.Column(db.Integer, db.ForeignKey('statuses.id'), nullable=False)
	role_id		= db.Column(db.Integer, db.ForeignKey('roles.id'), nullable=False)
	created 	= db.Column(db.DateTime, default=datetime.utcnow)
	updated 	= db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

	status 		= db.relationship('Status', backref='users', lazy=True)
	role 		= db.relationship('Role', backref='users', lazy=True)


	def check_password(self, password):
		return bcrypt.check_password_hash(self.password, password)


	@staticmethod
	def hash_password(password):
		return bcrypt.generate_password_hash(password)

	@staticmethod
	def generate_token(length=16):
		token = secrets.token_hex(16)
		if User.query.filter_by(token=token).first():
			return User.generate_token(length=length)
		return token

	def save(self):
		db.session.add(self)
		db.session.commit()

	def delete(self):
		db.session.delete(self)
		db.session.commit()

	def __repr__(self):
		return '<User %s>' % self.id


class Status(db.Model):
	__tablename__ = 'statuses'

	id			= db.Column(db.Integer, primary_key=True)
	name 		= db.Column(db.String(32), unique=True, nullable=False)

	def __repr__(self):
		return '<Status %s>' % self.id

	def __str__(self):
		return self.name

	

role_permission = db.Table(
	'roles_permissions',
	db.Column('role_id', db.Integer, db.ForeignKey('roles.id'), primary_key=True),
	db.Column('permission_id', db.Integer, db.ForeignKey('permissions.id'), primary_key=True)
)


class Role(db.Model):
	__tablename__ = 'roles'

	id			= db.Column(db.Integer, primary_key=True)
	name 		= db.Column(db.String(32), unique=True, nullable=False)
	desc 		= db.Column(db.String(256))

	def __repr__(self):
		return '<Role (%s)>' % self.name

	def __str__(self):
		return self.name

# op.bulk_insert(Role.__table__, [
# 	{'id':1, 'name': 'Owner'},
# 	{'id':2, 'name': 'Admin'},
# 	{'id':3, 'name': 'Other'}
# ])


# @db.event.listens_for(Role.__table__, 'after_create')
# def init_roles(*args, **kwargs):
# 	db.session.add(Role(name='Owner'))
# 	db.session.add(Role(name='Admin'))
# 	db.session.add(Role(name='Other'))
# 	db.session.commit()


class Permission(db.Model):
	__tablename__ = 'permissions'
	id			= db.Column(db.Integer, primary_key=True)
	name 		= db.Column(db.String(32), nullable=False)


	def __repr__(self):
		return '<Permission (%s)>' % self.name


