# Basic class to store app info (volatile at the moment)

class GetConfig:
	clicked = None  # username of who clicked the buzzer
	users = set()  # collection of all users

	@classmethod
	def add_user(cls, user, implied=False):
		if implied:
			print(f"User {user} registered implicitly")
		else:
			print(f"User {user} registered")
		cls.users.add(user)

	@classmethod
	def del_user(cls, user):
		if user in cls.users:
			print(f"User {user} logged out")
			cls.users.remove(user)
