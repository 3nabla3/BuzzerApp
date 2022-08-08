import pytest
from BuzzerApp import create_app


def test_favicon(app):
	resp = app.test_client().get('/favicon.ico')
	assert resp.status_code == 200


def test_index(client, auth):
	resp = client.get('/')
	# make sure it redirects to log in
	assert '/login' in resp.location

	resp = auth.login('test_user')
	assert 'test_user' in resp.headers['Set-Cookie']

