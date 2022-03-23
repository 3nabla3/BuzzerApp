class GetConfig:
	clicked = None
	users = set()

	@classmethod
	def add_user(cls, user):
		print(f"User {user} registered")
		cls.users.add(user)

	@classmethod
	def del_user(cls, user):
		print(f"User {user} logged out")
		if user in cls.users:
			cls.users.remove(user)
