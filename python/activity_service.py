###################################################
###################################################
#
#	Activity Tracker
#	by Francesco Burelli
#
###################################################
###################################################
import os.path
from datetime import datetime
import sqlite3
import math

class Service:
	def __init__(self, dbPath):
		# check if db exists
		first_time = os.path.isfile(dbPath) == False
		
		# connect or connect and create a new sqlite db
		self._connection = sqlite3.connect(dbPath)
		self._cursor = self._connection.cursor()
		
		if (first_time):
			# create the table
			query = '''CREATE TABLE activities (
				id INTEGER PRIMARY KEY,
				activity STRING NOT NULL,
				start_time LONG NOT NULL,
				end_time LONG
				)'''
			self._cursor.execute(query)
		
		self._record_id = None
		self.last_activity = None
		self.last_start_time = None
		self.current_activity = None
		
		self._updaterecordid()
	
	def _updaterecordid(self):
		result = self._cursor.execute(
			'''SELECT id, activity, start_time, end_time 
			FROM activities 
			ORDER BY start_time DESC 
			LIMIT 1''')
		row = result.fetchone()
		if (row):
			self._record_id = row[0]
			self.last_activity = row[1]
			self.last_start_time = row[2]
			# check if the activity is ended
			if (row[3] == None):
				# the activity is "running"
				self.current_activity = row[1]
	
	def start(self, activity):
		result_string = ''
		# check if activity is given
		if (activity == None or len(activity) == 0):
			# no activity, try to check the cache
			if (self.current_activity):
				# I have a current activity, that is the last activity also
				# I can't run a new blank activity
				return "INFO: " + self.current_activity + " just started"
			elif (self.last_activity):
				# I have a last activity, use it as activity to start
				activity = self.last_activity
			else:
				return "ERROR: no activity to start. Write an activity (e.g. start working)"
		
		if (self.current_activity and activity != self.current_activity):
			result_string += self.stop() + '\n'
		elif(self.current_activity == activity):
			# activity is currently running
			return "INFO: " + self.current_activity + " just started"
		
		self.current_activity = activity
		self.last_activity = activity
	
		# save the activity in the cache
		self.last_activity = activity
		self.current_activity = activity
		# save the activity record in the db
		date = datetime.utcnow()
		timestamp = int(date.timestamp())
		self._cursor.execute('INSERT INTO activities (activity, start_time) VALUES (?, ?)', (activity, timestamp))
		self._updaterecordid()
		
		result_string += "INFO: " + activity + " started at " + date.isoformat()
		return result_string
	
	def stop(self):
		if (self.current_activity == None):
			return "ERROR: no activity to stop"
		
		# update the activity in the cache
		ended_activity = self.current_activity
		self.current_activity = None
		
		# update the record in the db
		date = datetime.utcnow()
		timestamp = int(date.timestamp())
		self._cursor.execute('UPDATE activities SET end_time=? WHERE id=?', (timestamp, self._record_id))
		# and in cache
		self._record_id = None
		
		# calculate the activity tume
		seconds = timestamp - self.last_start_time
		return "INFO: " + ended_activity + " takes " + Service._durationstring(seconds) + " seconds"
	
	# mode:
	# 	all
	#	day
	#	week
	#	month (30 days)
	#	year  (360 days)
	def activities(self, mode='all', limit=10):
		interval = 60 * 60 * 24 * 360 * 100
		if (mode == 'day'):
			interval = 60 * 60 * 24
		elif (mode == 'week'):
			interval = 60 * 60 * 24 * 7
		elif (mode == 'month'):
			interval = 60 * 60 * 24 * 30
		elif (mode == 'year'):
			interval = 60 * 60 * 24 * 360
		result = self._cursor.execute(
			"""SELECT activity, SUM(end_time - start_time) as duration, start_time/? as s_time
			FROM activities 
			GROUP BY activity, s_time
			ORDER BY start_time DESC 
			LIMIT ?""", (interval,limit))
		result_string = "### activities ###\n"
		s_time = None
		while (True):
			row = result.fetchone()
			if (row == None):
				break
			if (row[1] == None):
				result_string += "\t" + row[0] + "\t\t" + "(current)" + "\n"
			else:
				if (s_time != row[2] and row[2] != None):
					s_time = row[2]
					date = datetime.fromtimestamp(s_time * interval)
					result_string += "\t --- from: " + date.isoformat() + " ---\n"
				
				result_string += "\t" + row[0] + "\t\t" + Service._durationstring(row[1]) + "\n"
		return result_string
	
	def _durationstring(duration):
		tmp = (60 * 60)
		hours = math.floor(duration / tmp)
		minutes = math.floor((duration / 60) - (hours * 60))
		seconds = math.floor(duration - (hours * tmp) - (minutes * 60))
		return str(hours) + " hours, " + str(minutes) + " minutes and " + str(seconds) + " seconds"
	
	def dispose(self):
		self._connection.commit()
		self._connection.close()
		