import sys
import re
from activity_service import Service

service = Service("activities.db")
		
def start(args):
	activity = None
	if (len(args) > 0):
		activity = args[0]
	
	return service.start(activity)

def stop(args):
	return service.stop()

def listactivities(args):
	if (len(args) > 0):
		return service.activities(args[0])
	else:
		return service.activities()

def helpf(args):
	return "HELP: try"

def askstopifneeds():
	if (service.current_activity):
		# ask to stop the current activity
		while (True):
			print ('Q: do you want to stop the current acrivity named "' + service.current_activity + '"? [Y/N]')
			# read command
			command_line = sys.stdin.readline()
			# execute the command
			if (command_line == "y\n" or command_line == "Y\n"):
				print (service.stop())
				break
			elif (command_line == "n\n" or command_line == "N\n"):
				break

def exit(args):
	askstopifneeds()
	
	service.dispose()
	sys.exit()
	
actions = {
	"start" :	start,
	"s"		:	start,
	"stop"	:	stop,
	"list"	:	listactivities,
	"l"		:	listactivities,
	"help"	:	helpf,
	"exit"	:	exit
}

while (True):
	print ("Q: Commands: start [ACTIVITY], stop, help, exit")
	
	command_line = sys.stdin.readline()
	
	command = re.split("[ ,\n]", command_line)
	
	if (command.count == 0):
		continue
	
	action = actions.get(command[0])
	
	if (action):
		del command[0]
		print (action(command))
	else:
		print ("ERROR: unknown command")