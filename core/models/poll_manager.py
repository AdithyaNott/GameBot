class PollManager:
	def __init__(self):
		self.polls = {}

	def create_poll():
		poll = new GamePoll()
		self.polls[poll.id] = poll
		return poll

	def get_poll(poll_id):
		if poll_id not in self.polls:
			return None
		return self.polls[poll_id]
