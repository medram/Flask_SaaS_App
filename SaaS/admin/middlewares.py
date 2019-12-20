from flask import redirect, url_for
from flask_login import current_user
from functools import wraps

def anonymous_required(f):
	@wraps(f)
	def decorated_func(*args, **kwargs):
		if current_user.is_authenticated:
			return redirect(url_for('admin.index'))
		return f(*args, **kwargs)
	return decorated_func