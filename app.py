import json
import os

from flask import Flask, render_template, request, flash, redirect, make_response, url_for, g

from api import api_bp
from config import GetConfig

app = Flask(__name__)
app.secret_key = os.urandom(12).hex()
app.register_blueprint(api_bp)


@app.errorhandler(404)
def not_found(_e):
	return redirect(url_for('index'))


@app.route('/')
def index():  # put application's code here
	if 'user' not in request.cookies:
		return redirect('login')

	if hasattr(GetConfig, 'clicked'):
		g.clicked = GetConfig.clicked

	data = json.dumps(list(GetConfig.users))
	return render_template('index.html', data=data)


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')

	user = request.form['user'].strip()
	if user == "":
		flash('Username cannot be empty!')
	elif user in GetConfig.users:
		flash('Username already taken!')
	else:
		resp = make_response(redirect(url_for('index')))
		resp.set_cookie('user', user)
		GetConfig.add_user(user)
		return resp

	return render_template('login.html')


@app.route('/logout', methods=['POST'])
def logout():
	resp = redirect(url_for('login'))
	user = request.cookies.get('user')
	GetConfig.del_user(user)
	resp.set_cookie('user', '', expires=0)

	return resp


if __name__ == '__main__':
	app.run()
