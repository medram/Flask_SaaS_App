import click

from run import manager
from flask_migrate import MigrateCommand

from SaaS.extensions import db
from SaaS.models import Setting
from SaaS.admin.models import Role, User, Status


# add migration commands to the manager.py
manager.add_command('db', MigrateCommand)

seeds_list = [
	# Roles
	Role(name='Owner'),
	Role(name='Admin'),
	Role(name='Other'),

	# Settings
	Setting(name='app_name', value='SaaS', autoload=True),
	Setting(name='default_timezone', value='Africa/Casablanca', autoload=True),

	# Admin account status
	Status(name='active'),
	Status(name='inactive'),

	# default admin.
	User(username='admin', email='admin@moakt.ws', password=User.hash_password('00112233'), status_id=1, role_id=1, token=User.generate_token())

]

@manager.command
def seeds():
	for i, seed in enumerate(seeds_list, 1):	
		try:
			db.session.add(seed)
			db.session.commit()
			click.secho(f'[*] Seed {i} is applied.', fg='green')
		except Exception as e:
			db.session.rollback()
			if not e.orig.args[1].startswith('Duplicate'):
				click.secho(f'[!] Seed {i} isn\'t applied!', fg='yellow')
				click.secho(f' |_ {e.orig.args[1]}', fg='red')
			else:
				click.secho(f'[!] Seed {i} is already applied!', fg='yellow')

	click.secho('Finished.', fg='bright_green')


if __name__ == '__main__':
	manager.run()