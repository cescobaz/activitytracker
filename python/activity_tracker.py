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

# start activity
def start(args):
	return service.start(*args)

# stop activity
def stop(args):
	return service.stop()

# show activities
def listactivities(args):
	return service.activities(*args)

# show help output
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
# ask to stop current acitivity
def askstopifneeds():
	if service.current_activity:
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

# exit application (ask to stop activity if needs)
def exit(args):
	askstopifneeds()
	
	service.dispose()
	sys.exit()

# map command string with function
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

# start main loop: ask for the command and execute it
while True:
	# print usage
	print ("Q: Commands: start [ACTIVITY], stop, help, exit")
	
	# read the command line and remove return char
	command_line = sys.stdin.readline()[:-1]
	
	# check it is not null
	if len(command_line) == 0:
		continue
	
	# split the command line
	command = re.split("[ ]+", command_line)
	
	# search the command
	action = actions.get(command[0])
	
	if action:
		# execute the command with arguments
		print (action(command[1:]))
	else:
		print ("ERROR: unknown command")