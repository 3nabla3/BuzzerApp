from flask import Flask, session, render_template, request, flash, redirect, make_response, url_for, g
from config import GetConfig

app = Flask(__name__)


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

	resp = make_response(redirect(url_for('index')))
	resp.set_cookie('user', user)

	return resp


@app.route('/logout', methods=['POST'])
def logout():
	resp = redirect(url_for('login'))

	if request.cookies.get('user'):
		resp.set_cookie('user', '', expires=0)

	return resp


@app.route('/click', methods=['POST'])
def click():
	if 'user' not in request.cookies:
		return 'no user logged in'

	if GetConfig.clicked is None:
		GetConfig.clicked = request.cookies['user']
		return f'pressed'

	return f'{GetConfig.clicked}'


@app.route('/reset', methods=['POST'])
def reset():
	GetConfig.clicked = None

	return f'reset'


if __name__ == '__main__':
	app.run()
