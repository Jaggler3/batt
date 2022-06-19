import sys
import os
import subprocess
import psutil

from webserver import Webserver
from context import Context

"""
bos-daemon
	-all core functionality connected to a webserver/port
	-creates file at /var/run/batt.pid

	-holds instance / instance set objects

	-bos can parse files and send to bos-daemon via POST /register
		-example post body:
		{
			action: config/service/event
			name: build-item-name
			entries: [
				for config, service -> "port=86"
				for event -> "command here"
			]
		}
		-registration entries will be digested based on the type of item
	
	-ecosystem changes
		- GET /dispatch
			-example dispatch query items
			{
				action: instance-create/instance-stop/run-event
				name: associated name
			}

	-ecosystem info
		- GET /overview
			-instance & service list
		- GET /interactions
			-interaction history
		- GET /dispatches
			-dispatch history with response & instances involved with each
		- GET /logs 
			-instance logs grouped by service

	-interaction
		- GET /get (predicate, route)
		- POST /post (predicate, route)
"""

INIT_PORT = 2332
PIDFILE_LOCATION = "/var/run/batt.pid"

def main():
	# check for already-running daemon
	
	# check for daemon pidfile
	if os.path.isfile(PIDFILE_LOCATION):
		# pidfile exists, read it and check if the pid is active
		pidContents = int(open(PIDFILE_LOCATION, "r").read())
		if psutil.pid_exists(pidContents):
			print("Daemon already running")
			return
	
	# start daemon
	print("Daemon is not yet running. Starting now...")

	# create / write pidfile
	newPid = str(os.getpid())
	writable = open(PIDFILE_LOCATION, "w")
	writable.write(newPid)
	writable.close()

	# open functionality to main port
	context = Context()
	server = Webserver(INIT_PORT, context)
	server.start()

if __name__ == '__main__':
	main()