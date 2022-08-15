# Contains the authentication endpoints

from flask import render_template, request, flash, \
	redirect, make_response, url_for, Blueprint

from BuzzerApp.config import GetConfig

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('auth/login/normal_login.html')

	# remove trailing whitespace on username
	user = request.form['user'].strip()

	if user == "":
		flash('Username cannot be empty!')
		code = 400  # bad request
	elif user in GetConfig.users:
		flash(f'Username {user} already taken!')
		code = 409  # conflict
	else:
		# register the user and set its cookie
		resp = make_response(redirect(url_for('buzz.index')))
		resp.set_cookie('user', user)
		GetConfig.add_user(user)
		return resp

	return render_template('auth/login/normal_login.html'), code


@auth_bp.route('/logout', methods=['POST'])
def logout():
	resp = redirect(url_for('auth.login'))
	# unregister the user and delete its cookie
	user = request.cookies.get('user')
	GetConfig.del_user(user)
	resp.set_cookie('user', '', expires=0)

	return resp


@auth_bp.route('/admin', methods=['GET', 'POST'])
def admin():
	if request.method == "GET":
		return render_template('auth/login/admin_login.html')
	return "admin post answer"
