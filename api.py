# import asyncio
import datetime
import json
from time import time, sleep

from flask import Blueprint, request, make_response, escape

from config import GetConfig

api = Blueprint('api', __name__)


@api.route('/click', methods=['POST'])
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


@api.route('/reset', methods=['POST'])
def reset():
	# reset all global config variables used in 'click'
	GetConfig.clicked = None
	GetConfig.clicks.clear()
	GetConfig.wait_until = None
	return 'reset'


@api.route('/wait-buzz', methods=['post'])
def wait_buzz():
	# wait until someone buzzes and return their username
	while GetConfig.clicked is None:
		sleep(0.3)

	return escape(GetConfig.clicked)


@api.route('/wait-reset', methods=['POST'])
def wait_reset():
	# wait until someone resets the buzzers
	while GetConfig.clicked is not None:
		sleep(0.3)
	return 'reset'


@api.route('/get-users', methods=['GET'])
def get_users():
	# return a json containing all the registered users
	sanitized = [escape(user) for user in GetConfig.users]

	resp = make_response(json.dumps(sanitized))
	resp.headers['Content-Type'] = 'application/json'
	return resp
