import os

from flask import Flask, render_template, request, flash,\
	redirect, make_response, url_for, g, send_file, escape

from api import api
from config import GetConfig

app = Flask(__name__)
app.secret_key = os.urandom(12).hex()
app.register_blueprint(api)


# redirect to the home page if the requested page does not exist
@app.errorhandler(404)
def not_found(_e):
	return redirect(url_for('index'))


# create a quick link to the icon image
@app.route('/favicon.ico')
def favicon():
	return send_file('./' + url_for('static', filename='buzzer.jpg'), mimetype='image/jpg')


@app.route('/')
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
	resp = make_response(render_template('index.html'))
	return resp


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		if 'user' in request.cookies and request.cookies['user'].strip() in GetConfig.users:
			return redirect(url_for('index'))
		return render_template('login.html')

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
		resp = make_response(redirect(url_for('index')))
		resp.set_cookie('user', user)
		GetConfig.add_user(user)
		return resp

	return render_template('login.html'), code


@app.route('/logout', methods=['POST'])
def logout():
	resp = redirect(url_for('login'))
	# unregister the user and delete its cookie
	user = request.cookies.get('user')
	GetConfig.del_user(user)
	resp.set_cookie('user', '', expires=0)

	return resp


# TODO: Make a special page that only an admin can view to kick users out and other privileged things


if __name__ == '__main__':
	app.run()
