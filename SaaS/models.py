from datetime import datetime
from SaaS.extensions import db

import SaaS.admin.models

class Setting(db.Model):
	__tablename__ = 'settings'

	id			= db.Column(db.Integer, primary_key=True)
	name 		= db.Column(db.String(32), nullable=False, unique=True)
	value 		= db.Column(db.Text)
	autoload	= db.Column(db.Boolean, default=False)

	def __repr__(self):
		return '<Setting (%s)>' % self.name


# @db.event.listens_for(Setting.__table__, 'after_create')
# def init_settings(*args, **kwargs):
# 	db.session.add(Setting(name='app_name', value='SaaS', autoload=True))
# 	db.session.add(Setting(name='default_timezone', value='Africa/Casablanca', autoload=True))
# 	db.session.commit()