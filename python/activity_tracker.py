###################################################
###################################################
#
#	Activity Tracker
#	by Francesco Burelli
#
###################################################
###################################################
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
	return '''HELP:\n
	\t- start, s [ACTIVITY]: start activity, if argument is missing then
	\t\tlast activity starts (if any). If a different activity is running
	\t\tthen this one will be stopped and the new one starts
	
	\t- stop: stop the current activity (if any)
	
	\t- list, l [group-by]: shows last activities grouped by \'gropu-by\'
	\t\tthat can be \'day\', \'week\' \'month\' or \'year\'
	
	\t- help: shows this output
	
	\t- exit: exits from this application. If an activity is running then
	\t\tit asks if you want to stop the current activity. You can exit from
	\t\tthe application while an activity is running and stop it at next usage.\n
				'''

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
	"h"		:	helpf,
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