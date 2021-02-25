from urllib.parse import parse_qs

class WebHandle:
	route = ""

	def __init__(self, route: str):
		super().__init__()
		self.route = route

	@staticmethod
	def get_one(items: list):
		if items == None:
			return None
		elif len(items) == 0:
			return None
		return items[0]

	def perform(self, request: dict):
		pass