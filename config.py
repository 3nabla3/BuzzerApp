class GetConfig:
	clicked = None
	users = set()

	@classmethod
	def add_user(cls, user):
		print(f"User {user} registered")
		cls.users.add(user)

	@classmethod
	def del_user(cls, user):
		if user in cls.users:
			print(f"User {user} logged out")
			cls.users.remove(user)
