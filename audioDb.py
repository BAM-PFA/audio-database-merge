#!/usr/bin/env python3
import mysql.connector
import os
import sys
import getpass
###################################
###################################

class DB:
	connection = None
	cursor = None

	def __init__(self,user):
		self.user = user

	def connect(self):
		# create a connection using root ... 
		if self.user == 'root':
			pw = getpass.getpass(prompt="enter password for mysql root:")
			self.connection = mysql.connector.connect(
				host='localhost',
				user='root',
				password=pw
				)
			return self.connection
		else:
			pass

	def query(self, sql,*args):
		cursor = None
		self.connection.autocommit = True
		try:
			self.connection.get_warnings = True
			cursor = self.connection.cursor()
			cursor.execute(sql,args)
		except mysql.connector.Error as e:
			print("Error! {}".format(e))
		
		return cursor

	def close_cursor(self):
		self.connection.cursor().close()

	def close_connection(self):
		self.connection.close()

###################################
###################################
def create_db(user):
	useAudioDB = "USE audio"
	try:
		connect = DB(user)
		connect.connect()
		# cursor = connect.query(createDbSQL)
		cursor = connect.close_cursor()
	except:
		print("Error: uh, error.. :(")
		sys.exit()
	
	cursor = connect.query(useAudioDB)
	print(cursor)
	createRecordingTable = ('''CREATE TABLE recordings(\
		recordingID INT(20) NOT NULL,\
		recordingPictionID VARCHAR(50),\
		recordingFilename VARCHAR(100),\
		recordingPermissions VARCHAR(200),\
		recordingDate VARCHAR(20),\
		recordingDay INT(10),\
		recordingMonth INT(10),\
		recordingYear INT(20),\
		recordingLocation VARCHAR(500),\
		recordingPFASeries VARCHAR(200),\
		recordingEventTitle VARCHAR(1000),\
		recordingEventNotes VARCHAR(1000),\
		recordingEventRecordingNotes VARCHAR(1000),\
		recordingTapeNumber VARCHAR(20),\
		recordingTapeSide VARCHAR(20),\
		recordingDigitizer VARCHAR(200),\
		recordingFileSize VARCHAR(50),\
		PRIMARY KEY (recordingID)\
		);\
	''')

	createBornDigitalStatusTable = ('''CREATE TABLE recordingDigitalStatus(
		recordingDigitalStatusID INT(20) NOT NULL AUTO_INCREMENT,\
		recordingDigitalStatusValue VARCHAR(20),\
		PRIMARY KEY (recordingDigitalStatusID)\
		);\
	''')

	insertDigiStatuses = ('''
		INSERT INTO recordingDigitalStatus(
			recordingDigitalStatusValue
			)
		VALUE (
			%s
			)

	''')

	createSpeakerTable = ('''CREATE TABLE speakers(\
		speakerID INT(20) NOT NULL,\
		speakerValue VARCHAR(1000),\
		PRIMARY KEY (speakerID)\
		);\
	''')

	createFilmTable = ('''CREATE TABLE filmTitles(\
		filmTitleID INT(20) NOT NULL,\
		filmTitleValue VARCHAR(1000),\
		PRIMARY KEY (filmTitleID)\
		);\
	''')

	createRecordingDigiStatus = ('''CREATE TABLE recording_digiStatus(\
		recordingID INT(20) NOT NULL,\
		recordingDigitalStatusID INT(20) NOT NULL,\
		FOREIGN KEY (recordingID) REFERENCES recordings(recordingID) ON DELETE CASCADE ON UPDATE CASCADE,\
		FOREIGN KEY (recordingDigitalStatusID) REFERENCES recordingDigitalStatus(recordingDigitalStatusID) ON DELETE CASCADE ON UPDATE CASCADE,\
		PRIMARY KEY (recordingID,recordingDigitalStatusID)\
		);\
	''')

	createRecordingSpeaker = ('''CREATE TABLE recording_speaker(\
		recordingID INT(20) NOT NULL,\
		speakerID INT(20) NOT NULL,\
		FOREIGN KEY (recordingID) REFERENCES recordings(recordingID) ON DELETE CASCADE ON UPDATE CASCADE,\
		FOREIGN KEY (speakerID) REFERENCES speakers(speakerID) ON DELETE CASCADE ON UPDATE CASCADE,\
		PRIMARY KEY (recordingID,speakerID)\
		);\
	''')

	createRecordingFilm = ('''CREATE TABLE recording_film(\
		recordingID INT(20) NOT NULL,\
		filmTitleID INT(20) NOT NULL,\
		FOREIGN KEY (recordingID) REFERENCES recordings(recordingID) ON DELETE CASCADE ON UPDATE CASCADE,\
		FOREIGN KEY (filmTitleID) REFERENCES filmTitles(filmTitleID) ON DELETE CASCADE ON UPDATE CASCADE,\
		PRIMARY KEY (recordingID,filmTitleID)\
		);\
	''')

	sqlToDo = [
		createRecordingTable,
		createSpeakerTable,
		createFilmTable,
		createBornDigitalStatusTable,
		createRecordingDigiStatus,
		createRecordingSpeaker,
		createRecordingFilm
		]

	for sql in sqlToDo:
		try:
			cursor = connect.query(sql)
			cursor = connect.close_cursor()
		except:
			print("mysql error... check your settings and try again.")
			sys.exit()
	try:
		for status in ["Born-digital","Digitized","Analog tape"]:
			cursor = connect.query(insertDigiStatuses,status)
		cursor = connect.close_cursor()	
	except:
		print("mysql error... check your settings and try again.")
		sys.exit()

def main():
	create_db('root')

if __name__ == "__main__":
	main()
	