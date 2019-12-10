from flask import Blueprint, render_template

main = Blueprint('home', __name__, template_folder='templates', static_folder='static')

@main.route('/')
def home():
	return 'Hello World!'

