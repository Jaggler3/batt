from urllib.parse import unquote, parse_qs

from context import Config, Context, Event, Service, ServiceAccess
from webhandle import WebHandle

def parseAccess(accessStr: str) -> int:
	string = accessStr.lower().strip()
	if string == "remote":
		return ServiceAccess.REMOTE
	if string == "local":
		return ServiceAccess.LOCAL
	return -1

class Register(WebHandle):
	def __init__(self, context: Context):
		super().__init__("/register", context)

	def perform(self, request: dict):
		action = WebHandle.get_one(request["action"])
		name = WebHandle.get_one(request["name"])
		entries = parse_qs(unquote(request["entry"]))

		# query requirements
		if action == None or name == None:
			return { "error": "/register requires an 'action' and 'name' query parameter" }
		
		# name validation
		if len(name) == 0:
			return { "error": "Invalid 'name' provided." }
		
		# create build item
		if action == "config":
			# build config item
			config_item = Config()
			config_item.name = name
			for k, v in entries:
				config_item.data[k] = WebHandle.get_one(v)

			# add item
			self.context.configs[config_item.name] = config_item
		elif action == "service":
			# build service item
			service_item = Service()
			service_item.name = name

			# location properties
			if "access" in entries:
				accessStr = WebHandle.get_one(entries["access"])
				accessType = parseAccess(accessStr)
				if accessType == -1:
					return { "error": "Invalid 'access' provided. `" + accessStr + "`" }
				service_item.location.access = accessType
			if "location" in entries:
				service_item.location.path = WebHandle.get_one(entries["location"])
			else:
				return { "error": "No 'location' provided for service `" + name + "`" }

			# routes
			if "routes" in entries:
				query_routes: str = WebHandle.get_one(entries["routes"])
				service_item.routes = query_routes.split(";")

			# whitelist
			if "whitelist" in entries:
				query_whitelist: str = WebHandle.get_one(entries["whitelist"])
				service_item.whitelist = query_whitelist.split(";")

			# command
			if "command" in entries:
				service_item.command = WebHandle.get_one(entries["command"])


			# add item
			self.context.services[service_item.name] = service_item		
		elif action == "event":
			event_item = Event()
			event_item.name = name

			# event actions
			if "commands" in entries:
				query_commands = WebHandle.get_one(entries["commands"])
				if query_commands:
					event_item.commands = query_commands.split(";")

			# add item
			self.context.events[event_item.name] = event_item
		else:
			return { "error": "Invalid 'action' provided. `" + action + "`" }


		return { "response": request }