class PollManager:
	def __init__(self):
		polls = {}

	def get_selected_choices_from_poll(poll_id):
		if poll_id not in polls:
			return None
		return polls[poll_id].selected_choices