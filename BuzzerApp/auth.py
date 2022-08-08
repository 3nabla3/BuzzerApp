# Contains the main endpoints like the index page and log-in page

from flask import render_template, request, flash, \
	redirect, make_response, url_for, g, send_file, Blueprint

from BuzzerApp.config import GetConfig

auth_bp = Blueprint('auth', __name__)


# create a quick link to the icon image
@auth_bp.route('/favicon.ico')
def favicon():
	return send_file('./' + url_for('static', filename='buzzer.jpg'), mimetype='image/jpg')


@auth_bp.route('/')
def index():
	# if the user is not logged in, redirect to the login page
	if 'user' not in request.cookies:
		return redirect('login', code=307)

	# if the cookie is valid but the user isn't registered within the app,
	# implicitly register the user
	user = request.cookies['user']
	if user not in GetConfig.users:
		GetConfig.add_user(user, implied=True)

	# set this for use in jinja parsing
	g.clicked = GetConfig.clicked
	resp = make_response(render_template('auth/index.html'))
	return resp


@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('auth/login.html')

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
		resp = make_response(redirect(url_for('auth.index')))
		resp.set_cookie('user', user)
		GetConfig.add_user(user)
		return resp

	return render_template('auth/login.html'), code


@auth_bp.route('/logout', methods=['POST'])
def logout():
	resp = redirect(url_for('auth.login'))
	# unregister the user and delete its cookie
	user = request.cookies.get('user')
	GetConfig.del_user(user)
	resp.set_cookie('user', '', expires=0)

	return resp

# TODO: Make a special page that only an admin can view to kick users out and other privileged things
