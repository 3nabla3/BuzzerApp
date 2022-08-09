import pytest


def test_favicon(app):
	resp = app.test_client().get('/favicon.ico')
	assert resp.status_code == 200


def test_index(client, auth):
	resp = client.get('/')
	# make sure it redirects to log in
	assert '/login' in resp.location

	# test implicit registration
	client.set_cookie('localhost', 'user', 'test_impl_user')
	resp = client.get('/')
	# make sure there is no redirect
	assert resp.location is None
	assert resp.status_code == 200


def test_login_get(client):
	resp = client.get('/login')
	assert b'login' in resp.data
	# make sure there is no redirect, just the page is shown
	assert resp.location is None


@pytest.mark.parametrize(("username", "message", "code", "cookie"), (
	("", "cannot be empty", 400, None),
	("test_user1", "Redirecting", 302, "test_user1"),
	("test_user1", "already taken", 409, None),
	("test_user2", "Redirecting", 302, "test_user2")
	)
)
def test_login_post(client, username, message, code, cookie):
	# post request
	resp = client.post('/login', data={'user': username})
	assert message in str(resp.data)
	assert code == resp.status_code
	if cookie is not None:
		assert cookie in resp.headers['Set-Cookie']


def test_logout(client, auth):
	auth.login('test_user3')
	assert client.get('/').status_code == 200

	auth.logout()
	resp = client.get('/')
	assert resp.status_code == 307
	assert '/login' in resp.location

