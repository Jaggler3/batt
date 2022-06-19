from webhandle import WebHandle
from context import Context

class Dispatch(WebHandle):
	def __init__(self, context: Context):
		super().__init__("/dispatch", context)

	def perform(self, request: dict):
		action = request["action"]
		name = request["name"]
		
		return { "response": request }