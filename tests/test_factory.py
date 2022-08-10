import pytest
from BuzzerApp import create_app


def test_config():
	assert not create_app().testing
	assert create_app({'TESTING': True}).testing


def test_error_handler():
	resp = create_app().test_client().get('path/that/does/not/exist')
	# make sure it redirects to index
	assert '/' == resp.location[-1]
