from dotenv import load_dotenv
load_dotenv()

from SaaS import create_app
from flask_script import Manager

# get flask application.
app = create_app()

# init manager.
manager = Manager(app)

if __name__ == '__main__':
	app.run(
		host=app.config.get('HOST', '127.0.0.1'), 
		port=int(app.config.get('PORT') if app.config.get('PORT') else 5000), 
		debug=bool(app.config.get('DEBUG', False))
	)