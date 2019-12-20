# import click
# import time
# import random
# from functools import wraps

# class User():
# 	def __init__(self, name):
# 		self.name = name
# 		self.role = 'user'

# current_user = User('Mohammed')

# def role_required(*roles):
# 	def decorator(f):
# 		def decorated_function(*args, **kwargs):
# 			print('> role_required')
# 			# TODO: do the check.
# 			return f(*args, **kwargs)
# 		return decorated_function
# 	return decorator


# def login_required():
# 	def decorator(f):
# 		def decorated_function(*args, **kwargs):
# 			print('> login_required')
# 			# TODO: Do the check.
# 			return f(*args, **kwargs)
# 		return decorated_function
# 	return decorator


# def logger(f):
# 	print('logger...')
# 	@wraps(f)
# 	def decorated_func(*args, **kwargs):
# 		print('logging "{}" function {:016X}.'.format(f.__name__, id(f)))
# 		return f(*args, **kwargs)
# 	return decorated_func


# def notify(f):
# 	print('notify...')
# 	@wraps(f)
# 	def decorated_func(*args, **kwargs):
# 		print('notifying , "{}" function {:016X}.'.format(f.__name__, id(f)))
# 		return f(*args, **kwargs)
# 	return decorated_func


# @notify
# @logger
# def download(image):
# 	print(f'Downloading {image} ...0x{id(download):016X}')

# def main():
# 	download('logo.png')

# if __name__ == '__main__':
# 	main()
