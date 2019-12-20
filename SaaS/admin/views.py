from flask import Blueprint, render_template, request, flash, \
				abort, escape, redirect, url_for, jsonify
from .forms import LoginForm, AddUserForm, EditUserForm
from .models import User
from .middlewares import anonymous_required 
from ..extensions import login_manager, db

from flask_login import login_user, logout_user, login_required, current_user


# init login manager here.
login_manager.login_view = 'admin.login'
login_manager.login_message = 'Please log in to access this page.'
login_manager.login_message_category = 'info'

# Admin blueprint
admin = Blueprint('admin', __name__, url_prefix='/admin', template_folder='templates', static_folder='static')


@admin.route('/')
@login_required
def index():
	return render_template('dashboard/index.html', page_title='Dashboard')


@admin.route('/login', methods=['GET', 'POST'])
@anonymous_required
def login():
	form = LoginForm()
	if form.validate_on_submit():
		user = User.query.filter_by(email=form.email.data).first()
		if user and user.check_password(form.password.data):
			login_user(user, form.remember.data)

			next = request.args.get('next')
			if next:
				flash('Logged in successfully.', 'success')
			return redirect(next or url_for('admin.index'))
		else:
			flash('Oops, Your email/password is invalid.', 'warning')

	return render_template('login.html', form=form, page_title='Users')



@admin.route('users/add', methods=['GET', 'POST'])
@login_required
def add_user():
	form = AddUserForm(request.form)
	#print(form.__dict__['_fields'].__dir__(), flush=True)
	if form.validate_on_submit():
		user = User()
		user.username = form.username.data
		user.email = form.email.data
		user.password = User.hash_password(form.password.data)
		user.token = User.generate_token()
		user.status_id = form.status.data.id
		user.role_id = form.role.data.id
		user.save()
		
		flash('Created Successfully.', 'success')
		return redirect(url_for('admin.users'))

	return render_template('dashboard/add_user.html', page_title='Add user', form=form)



@admin.route('/users/edit/<int:uid>', methods=['GET', 'POST'])
@login_required
def edit_user(uid):
	user = User.query.filter_by(id=uid).first()

	if not user:
		flash(f'User not found.', 'warning')
		return redirect(url_for('admin.users'))

	form = EditUserForm(request.form, obj=user)
	if form.validate_on_submit():
		# Adding custom validation
		if user.email != form.email.data:
			if User.query.filter_by(email=form.email.data).first():
				flash('This Email has been already taken.', 'warning')
				return redirect(url_for('admin.edit_user', uid=user.id))
		
		# hash the password if found
		if form.password.data != '':
			user.password = User.hash_password(form.password.data)

		user.username = form.username.data
		user.email = form.email.data
		user.status_id = form.status.data.id
		user.role_id = form.role.data.id
		user.save()

		flash('Updated Successfully.', 'success')
		return redirect(url_for('admin.users'))		

	if request.method == 'GET':
		form.password.data = ''

	return render_template('dashboard/edit_user.html', page_title='Edit user', form=form, user=user)



@admin.route('/users')
@login_required
def users():
	page = request.args.get('page', 1, int)
	per_page = 2
	users_pagination = User.query.order_by(User.id.desc()).paginate(page, per_page, error_out=False)

	crud_config = {
		'vocab' :	('users', 'user'),
		'add_item_route': 'admin.add_user',
		'edit_item_route': 'admin.edit_user',
		'del_item_route': 'admin.delete_user',
		'pagination': users_pagination
	}

	return render_template('dashboard/users.html', page_title='Users', crud_config=crud_config)



@admin.route('/users/del/<int:uid>', methods=['DELETE'])
@login_required
def delete_user(uid):
	#TODO: check permissions first.
	try:
		user = User.query.filter_by(id=uid).first()
		if user:
			user.delete()
			return jsonify({'status': True, 'message': 'Deleted Successfully.'})
	except Exception as e:
		print(e, flush=True)
		return jsonify({'status': False, 'error': 'Something went wrong.'}), 500


@admin.route('/logout')
@login_required
def logout():
	logout_user()
	return redirect(url_for('admin.login'))

