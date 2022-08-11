import pytest
from BuzzerApp import create_app


@pytest.fixture()
def app():
	app = create_app({'TESTING': True})
	return app


@pytest.fixture()
def client(app):
	return app.test_client()


class AuthActions:
	def __init__(self, client):
		self._client = client

	def login(self, user):
		return self._client.post('/auth/login', data={'user': user})

	def logout(self):
		return self._client.post('/auth/logout')


@pytest.fixture()
def auth(client):
	return AuthActions(client)
