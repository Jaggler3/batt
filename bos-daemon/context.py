class Context:
	# all items can be accessed by their name in a dict collection
	instances: dict = {}
	services: dict = {}
	configs: dict = {}
	events: dict = {}

	def __init__(self):
		super().__init__()

class BattItem:
	name: str

class Instance(BattItem):
	name: str = ""
	pid: int = -1
	service: str = ""
	status: str = ""
	port: int = -1

class Config(BattItem):
	data: dict = {}

class ServiceAccess:
	REMOTE = 0
	LOCAL = 1

class ServiceLocation:
	# Either the local runnable path or the TCP host name, depending on access type
	path: str = ""
	# ServiceAccess.REMOTE or ServiceAccess.LOCAL
	access: int = -1

class Service(BattItem):
	location: ServiceLocation = ServiceLocation()
	routes: list[str] = []
	whitelist: list[str] = []
	command: str = ""

class Event(BattItem):
	commands: list[str] = []