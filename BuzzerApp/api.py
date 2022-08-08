# Contains the endpoints that change the state of the server
# and the endpoint to get the logged-in users

import datetime
import json
from time import sleep

from flask import Blueprint, request, make_response, escape

from BuzzerApp.config import GetConfig

api_bp = Blueprint('api', __name__)


@api_bp.route('/click', methods=['POST'])
def click():
	if 'user' not in request.cookies:
		return 'no user logged in', 400  # bad request

	user = request.cookies['user']
	print(f"Got click by {user}")

	# if the button was already pressed, return the name
	if GetConfig.clicked:
		return escape(GetConfig.clicked)

	GetConfig.clicked = user
	return "pressed"


@api_bp.route('/reset', methods=['POST'])
def reset():
	# reset who clicked the buzzer
	GetConfig.clicked = None
	return 'reset'


@api_bp.route('/wait-buzz', methods=['POST'])
def wait_buzz():
	# wait until someone buzzes and return their username
	while GetConfig.clicked is None:
		sleep(0.3)
	return escape(GetConfig.clicked)


@api_bp.route('/wait-reset', methods=['POST'])
def wait_reset():
	# wait until someone resets the buzzers
	while GetConfig.clicked is not None:
		sleep(0.3)
	return 'reset'


@api_bp.route('/get-users', methods=['GET'])
def get_users():
	# return a json containing all the registered users
	sanitized = [escape(user) for user in GetConfig.users]

	resp = make_response(json.dumps(sanitized))
	resp.headers['Content-Type'] = 'application/json'
	return resp
