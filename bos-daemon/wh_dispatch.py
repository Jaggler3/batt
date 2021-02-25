from webhandle import WebHandle

class Dispatch(WebHandle):
	def __init__(self):
		super().__init__("/dispatch")

	def perform(self, request: dict):
		action = request["action"]
		name = request["name"]
		
		return { "response": request }