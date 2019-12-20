from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, IntegerField, DateTimeField, SubmitField
from wtforms.validators import DataRequired, Email, ValidationError, Required
from wtforms.ext.sqlalchemy.orm import model_form

from flask_login import current_user

from ..extensions import db
from .models import User


############################# Login Form #############################
class LoginForm(FlaskForm):
	email = StringField('Email', validators=[DataRequired(), Email()])
	password = PasswordField('Password', validators=[DataRequired()])
	remember = BooleanField('Remember Me')
	submit = SubmitField('Login')


############################# Create User Form #############################
# check if the inserted email if is available
def add_check_email(form, email):
	if User.query.filter_by(email=email.data).first():
		raise ValidationError('This Email has been already taken.')

AddUserForm = model_form(User, base_class=FlaskForm, exclude=['status_id', 'role_id', 'token', 'created', 'updated'], db_session=db.session)
AddUserForm.submit = SubmitField('Create user')
AddUserForm.email.kwargs['validators'].extend([Email(), add_check_email])


############################# Edit User Form ###############################
EditUserForm = model_form(User, base_class=FlaskForm, exclude=['status_id', 'role_id', 'token', 'created', 'updated'], db_session=db.session)
EditUserForm.submit = SubmitField('Update')
EditUserForm.email.kwargs['validators'].extend([Email()])
try:
	# delete the required validator
	EditUserForm.password.kwargs['validators'].pop(0)
except ValueError:
	pass