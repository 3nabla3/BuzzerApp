# import asyncio
import datetime
import json
from time import time, sleep

from flask import Blueprint, request, make_response, escape

from config import GetConfig

api = Blueprint('api', __name__)


# TODO: make sure the timestamp seems legit before accepting it as valid
# TODO: should I really accept timestamps?
#  1s off on a clock can make a huge difference
@api.route('/click', methods=['POST'])
def click():
	if 'user' not in request.cookies:
		return 'no user logged in', 400  # bad request
	if 'ts' not in request.form:
		return 'no timestamp provided', 400

	# extract the user and timestamp from post form
	user = request.cookies['user']
	ts = float(request.form['ts'])

	# register the user's click
	GetConfig.clicks[ts] = user
	print(f"Got click by {user} at {datetime.datetime.fromtimestamp(ts)}")

	# if there is no wait deadline set yet, set it 'time_delay' seconds ahead of the request's timestamp
	if GetConfig.wait_until is None:
		GetConfig.wait_until = ts + GetConfig.time_delay

	# wait for 'time_delay' seconds before continuing
	# to wait for potential previous clicks that lagged behind
	while time() < GetConfig.wait_until:
		sleep(0.01)

	# find the first click out of all the registered clicks
	lowest_ts = min(GetConfig.clicks.keys())

	# if this is the tread of the fastest player, it sets its username as the winner
	if lowest_ts == ts:
		GetConfig.clicked = user
		print(f"All clicks: {GetConfig.clicks}")
		print(f"First click by {GetConfig.clicked}")
		return 'pressed'

	# if not, return the username of the winner
	return escape(GetConfig.clicked)


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
