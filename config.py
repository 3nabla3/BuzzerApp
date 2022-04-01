class GetConfig:
	clicked = None  # username of who clicked the buzzer
	users = set()  # collection of all users

	# record the timestamps of all buzzes 'time_delay' seconds after the first one is received
	# to account for lag or network latency
	time_delay = 3
	clicks = {}  # collection of all clicks while the server is delaying
	wait_until = None  # timestamp until the delay is over

	@classmethod
	def add_user(cls, user):
		print(f"User {user} registered")
		cls.users.add(user)

	@classmethod
	def del_user(cls, user):
		if user in cls.users:
			print(f"User {user} logged out")
			cls.users.remove(user)
