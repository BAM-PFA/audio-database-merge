#!/usr/bin/env python3
import json
import sys

from audioDbBuilder import DB as DB

'''
This takes the normalized JSON object and inserts records for
each item.
See audioNormalizer.py for the JSON structure.
'''

useAudioDB = "USE audio"

insertRecording = (
	'''
	INSERT IGNORE INTO recordings(
		recordingID,
		recordingPictionID,
		recordingFilename,
		recordingPermissions,
		recordingDate,
		recordingDay,
		recordingMonth,
		recordingYear,
		recordingLocation,
		recordingPFASeries,
		recordingEventTitle,
		recordingEventNotes,
		recordingEventRecordingNotes,
		recordingTapeNumber,
		recordingTapeSide,
		recordingDigitizer,
		recordingFileSize
		)
	VALUES (
		%s,
		%s,
		%s,
		%s,
		%s,
		%s,
		%s,
		%s,
		%s,
		%s,
		%s,
		%s,
		%s,
		%s,
		%s,
		%s,
		%s
		)
	'''
	)

insertSpeaker = (
	'''
	INSERT INTO speakers(
		speakerID,
		speakerValue
		)
	VALUES (
		%s,
		%s
		)
	'''
	)

insertFilmTitle = (
	'''
	INSERT INTO filmTitles(
		filmTitleID,
		filmTitleValue
		)
	VALUES (
		%s,
		%s
		)
	'''
	)

insertDigiStatus = (
	'''
	INSERT INTO recording_digiStatus(
		recordingID,
		recordingDigitalStatusID
		)
	VALUES (
		%s,
		%s
		)
	'''
	)

insertRecordingSpeaker = (
	'''
	INSERT INTO recording_speaker(
		recordingID,
		speakerID
		)
	VALUES (
		%s,
		%s
		)
	'''
	)

insertRecordingFilm = (
	'''
	INSERT INTO recording_film(
		recordingID,
		filmTitleID
		)
	VALUES (
		%s,
		%s
		)
	'''
	)

digitalStatuses = {
	'Born-digital':1,
	'Digitized':2,
	'Analog tape':3	
}

def add_speakers(data,connect):
	for speakerID in data['speakers']:
		speaker = data['speakers'][speakerID]['speakerValue']
		data['speakers'][speakerID]
		try:
			cursor = connect.query(
				insertSpeaker,
				speakerID,
				speaker
				)
		except:
			print("GAH SPEAKER "+speakerID)
			sys.exit()

def add_filmTitles(data,connect):
	for filmTitleID in data['filmTitles']:
		filmTitle = data['filmTitles'][filmTitleID]['filmTitleValue']
		print(data['filmTitles'][filmTitleID])
		try:
			cursor = connect.query(
				insertFilmTitle,
				filmTitleID,
				filmTitle
				)
		except:
			print("GAH FILM TITLE "+filmTitleID)
			sys.exit()


def add_recordings(data,connect):
	cursor = connect.query(useAudioDB)
	for recordingID in data['recordings']:
		recording = data['recordings'][recordingID]
		digiStatus = digitalStatuses[recording['digitalStatus']]
		print(recording)
		try:
			connect.query(
				insertRecording,
				recordingID,
				recording['pictionID'],
				recording['filename'],
				recording['permissions'],
				recording['date'],
				recording['day'],
				recording['month'],
				recording['year'],
				recording['location'],
				recording['pfaSeries'],
				recording['eventTitle'],
				recording['eventNotes'],
				recording['eventRecordingNotes'],
				recording['tapeNumber'],
				recording['tapeSide'],
				# recording['digitalStatus'],
				recording['digitizer'],
				recording['fileSize']
				)
			connect.close_cursor()
			
			connect.query(
				insertDigiStatus,
				recordingID,
				digiStatus
				)
			connect.close_cursor()
			for speakerID in recording['speakers']:
				# iterate over the list of speakers 
				# add a record to the join table for recordingID,speakerID
				try:
					connect.query(
						insertRecordingSpeaker,
						recordingID,
						speakerID
						)
					connect.close_cursor()
				except:
					print("can't create record for conection"
						" btw {} and {}".format(speakerID,recordingID))
			for filmTitleID in recording['filmTitles']:
				# iterate over the list of film titles 
				# add a record to the join table for recordingID,filmID
				try:
					connect.query(
						insertRecordingFilm,
						recordingID,
						filmTitleID
						)
					connect.close_cursor()
				except:
					print("can't create record for conection"
						" btw {} and {}".format(filmTitleID,recordingID))
		except:
			print("GAH")
			sys.exit()
	print("ALL DONE")

def main():
	with open('data_files/combined-audio-data-cleaned.json','r') as f:
		data = json.load(f)

	try:
		connect = DB("root")
		connect.connect()
		cursor = connect.close_cursor()
	except:
		print("Error: uh, error.. :(")
		sys.exit()
	
	cursor = connect.query(useAudioDB)
	add_speakers(data,connect)
	add_filmTitles(data,connect)
	add_recordings(data,connect)

if __name__ == "__main__":
	main()
