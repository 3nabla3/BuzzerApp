# contains the app factory
from flask import Flask, redirect, url_for
import os


def create_app(test_config=None):
	app = Flask(__name__, instance_relative_config=True)
	app.secret_key = os.urandom(12).hex()

	@app.errorhandler(404)
	def not_found(_e):
		return redirect(url_for('auth.index'))

	from BuzzerApp.auth import auth_bp
	app.register_blueprint(auth_bp)

	from BuzzerApp.api import api_bp
	app.register_blueprint(api_bp)

	if test_config is not None:
		app.config.from_mapping(test_config)
	else:
		app.config.from_mapping({
			'TESTING': False
		})

	return app
