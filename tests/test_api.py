import unittest
from flask import Flask


class MyTestCase(unittest.TestCase):
	def test_click(self):
		app = Flask(__name__)
		app.testing = True
		client = app.test_client()


if __name__ == '__main__':
	unittest.main()
