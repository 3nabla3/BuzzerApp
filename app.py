import json
import os
import time

from flask import Flask, render_template, request, flash, redirect, make_response, url_for, g
from config import GetConfig

app = Flask(__name__)
app.secret_key = os.urandom(12).hex()


@app.route('/')
def index():  # put application's code here
	if 'user' not in request.cookies:
		return redirect('login')

	if hasattr(GetConfig, 'clicked'):
		g.clicked = GetConfig.clicked

	return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
	if request.method == 'GET':
		return render_template('login.html')

	user = request.form['user']
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


@app.route('/click', methods=['POST'])
def click():
	if 'user' not in request.cookies:
		return 'no user logged in'

	user = request.cookies['user']

	if GetConfig.clicked is None or GetConfig.clicked == user:
		GetConfig.clicked = user
		return 'pressed'

	return f'{GetConfig.clicked}'


@app.route('/reset', methods=['POST'])
def reset():
	GetConfig.clicked = None
	return 'reset'


@app.route('/wait-buzz', methods=['post'])
def wait_buzz():
	while GetConfig.clicked is None:
		time.sleep(0.3)

	return GetConfig.clicked


@app.route('/wait-reset', methods=['POST'])
def wait_reset():
	while GetConfig.clicked is not None:
		time.sleep(0.3)

	return 'reset'


@app.route('/get-users', methods=['GET'])
def get_users():
	return json.dumps(GetConfig.users)


if __name__ == '__main__':
	app.run()
