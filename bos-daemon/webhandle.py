from urllib.parse import parse_qs

from context import Context

class WebHandle:
	route: str
	context: Context

	def __init__(self, route: str, context: Context):
		super().__init__()
		self.route = route
		self.context = context

	@staticmethod
	def get_one(items: "list[str]"):
		if items == None:
			return None
		elif len(items) == 0:
			return None
		return items[0]

	def perform(self, request: dict):
		pass