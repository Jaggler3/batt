import http.server
import socketserver
from urllib.parse import urlparse, parse_qs, ParseResult
import json

from webhandle import WebHandle
from wh_dispatch import Dispatch
from wh_register import Register

class Webserver:
	def __init__(self, port, context):
		self.handler = RequestHandlerGenerator(context).generate()
		self.port = port
		self.tcpServer = socketserver.TCPServer(("", self.port), self.handler)
		pass

	def start(self):
		self.tcpServer.serve_forever()
		return self

	def end(self):
		pass

class ErrorHandle(WebHandle):
	def __init__(self):
		super().__init__("/error")
	
	def perform(self, request) -> dict:
		return { "status": "error" }

class RequestHandlerGenerator():
	def __init__(self, context):
		self.context = context

	def generate(self):
		localContext = self.context

		endpoints: list[WebHandle] = [
			Dispatch(self.context),
			Register(self.context)
		]

		class HttpRequestHandler(http.server.SimpleHTTPRequestHandler):
			def do_GET(self):
				# Sending an '200 OK' response
				self.send_response(200)

				# Setting the header
				self.send_header("Content-type", "application/json")

				# Whenever using 'send_header', you also have to call 'end_headers'
				self.end_headers()

				request: ParseResult = urlparse(self.path)

				handle: WebHandle = None

				for item in endpoints:
					if item.route == request.path:
						handle = item
						break

				if handle == None:
					handle = ErrorHandle()

				output = handle.perform(parse_qs(request.query))

				self.wfile.write(bytes(json.dumps(output), "utf8"))

				return
		return HttpRequestHandler
