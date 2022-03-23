class GetConfig:
	clicked = None
	users = set()

	@classmethod
	def add_user(cls, user):
		cls.users.add(user)

	@classmethod
	def del_user(cls, user):
		cls.users.remove(user)
