# contains the main endpoints like the index

from flask import Blueprint, url_for, send_file, request, redirect,\
	make_response, render_template, g

from BuzzerApp.config import GetConfig

buzzer_bp = Blueprint('buzz', __name__,)


# create a quick link to the icon image
@buzzer_bp.route('/favicon.ico')
def favicon():
	return send_file('.' + url_for('static', filename='buzzer.png'), mimetype='image/jpg')


@buzzer_bp.route('/')
def index():
	# if the user is not logged in, redirect to the login page
	if 'user' not in request.cookies:
		return redirect(url_for('auth.login'), code=307)

	# if the cookie is valid but the user isn't registered within the app,
	# implicitly register the user
	user = request.cookies['user']
	if user not in GetConfig.users:
		GetConfig.add_user(user, implied=True)

	# set this for use in jinja parsing
	g.clicked = GetConfig.clicked
	resp = make_response(render_template('auth/index.html'))
	return resp
