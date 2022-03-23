import asyncio
import json
import time

from flask import Blueprint, request, make_response

from config import GetConfig

api_bp = Blueprint('api', __name__)


@api_bp.route('/click', methods=['POST'])
def click():
	if 'user' not in request.cookies:
		return 'no user logged in'

	user = request.cookies['user']

	if GetConfig.clicked is None or GetConfig.clicked == user:
		GetConfig.clicked = user
		return 'pressed'

	return f'{GetConfig.clicked}'


@api_bp.route('/reset', methods=['POST'])
def reset():
	GetConfig.clicked = None
	return 'reset'


@api_bp.route('/wait-buzz', methods=['post'])
async def wait_buzz():
	while GetConfig.clicked is None:
		await asyncio.sleep(0.3)

	return GetConfig.clicked


@api_bp.route('/wait-reset', methods=['POST'])
async def wait_reset():
	while GetConfig.clicked is not None:
		await asyncio.sleep(0.3)

	return 'reset'


@api_bp.route('/get-users', methods=['GET'])
def get_users():
	resp = make_response(json.dumps(list(GetConfig.users)))
	resp.headers['Content-Type'] = 'application/json'
	return resp
