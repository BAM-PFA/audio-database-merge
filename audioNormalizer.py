#!/usr/bin/env python3
import csv
import json
'''
This takes a CSV with one row per recording, that could have
an arbitrary number of columns for speakers and related film titles,
parses those related entities out, and creates a JSON object
with a dict per entity type. Each type will become a table in the
MySQL database.
'''
output = {
	# the basic record for the db will be a 'recording' 
	# with these attributes:
	'recordings' : {
		# 'pk_recordingID' : {
		# 	'speakers' : [],
		# 	'filmTitles' : [],
		# 	'pictionID' : '',
		# 	'filename' : '',
		# 	'permissions' : '',
		# 	'date' : '',
		# 	'day' : '',
		# 	'month' : '',
		# 	'year' : '',
		# 	'location' : '',
		# 	'pfaSeries' : '',
		#	'eventTitle' : '',	
		# 	'eventNotes' : '',
		#	'eventRecordingNotes' : ''
		# 	'tapeNumber' : '',
		# 	'tapeSide' : '',
		# 	'digitaStatus' : '',
		# 	'digitizer' : '',
		# 	'fileSize' : '',
		# }
	},
	# each speaker is just a string of the complete personal or corporate name
	'speakers' : {
		# 'pk_speakerID' : {
		# 	'speakerValue' : '',
		# 	'fk_usedBy' : []
		# }
	},
	'filmTitles' : {
		# 'pk_filmID' : {
		# 	'filmTitleValue' : '',
		# 	'fk_usedBy' : []
		# }
	}
}

# these two counters start the speaker & film title ID sequences
speakersCounter = 1
filmTitlesCounter = 1
# start dicts of unique speakers and film titles to reference
# when building a recording record
existingSpeakers = {}
existingFilmTitles = {}

with open('data_files/combined-audio-data-cleaned.csv','r') as f:
	reader = csv.DictReader(f)
	for row in reader:
		# the event ID is sequential from the combined CSV
		recordingID = row['event ID']
		output['recordings'][recordingID] = {}
		# these lists will include the ID of each speaker and film title
		# referenced in the recording
		output['recordings'][recordingID]['speakers'] = []
		output['recordings'][recordingID]['filmTitles'] = []

		output['recordings'][recordingID]['pictionID'] = row['piction ID']
		output['recordings'][recordingID]['filename'] = row['filename']
		output['recordings'][recordingID]['permissions'] = row['permissions']
		output['recordings'][recordingID]['date'] = row['iso 8601']
		output['recordings'][recordingID]['day'] = row['day']
		output['recordings'][recordingID]['month'] = row['month']
		output['recordings'][recordingID]['year'] = row['year']
		output['recordings'][recordingID]['location'] = row['recording location']
		output['recordings'][recordingID]['pfaSeries'] = row['pfa series']
		output['recordings'][recordingID]['eventTitle'] = row['event title']
		output['recordings'][recordingID]['eventNotes'] = row['event notes']
		output['recordings'][recordingID]['eventRecordingNotes'] = row['technical/recording notes']
		output['recordings'][recordingID]['tapeNumber'] = row['tape number']
		output['recordings'][recordingID]['tapeSide'] = row['tape side']
		output['recordings'][recordingID]['digitalStatus'] = row['Born-digital status']
		output['recordings'][recordingID]['digitizer'] = row['digitizer']
		output['recordings'][recordingID]['fileSize'] = row['file size']
		
		for key in row.keys():
			if not row[key] == '':
				theName = row[key]
				if key.startswith('speakers'):
					# for each SPEAKER column, add the value to the recording
					# and also increment the speaker counter
					if not theName in existingSpeakers:
						output['speakers'][speakersCounter] = {}
						output['speakers'][speakersCounter]['fk_usedBy'] = []
						output['speakers'][speakersCounter]['speakerValue'] = theName
						output['speakers'][speakersCounter]['fk_usedBy'].append(row['event ID'])
						existingSpeakers[theName] = speakersCounter
						output['recordings'][recordingID]['speakers'].append(str(speakersCounter))
						speakersCounter += 1
					else:
						# or if the speaker already exists, just add the 
						theSpeakerID = existingSpeakers[theName]
						output['recordings'][recordingID]['speakers'].append(str(theSpeakerID))
						output['speakers'][theSpeakerID]['fk_usedBy'].append(row['event ID'])
				elif key.startswith('film'):
					# do the same for films as for speakers
					if not theName in existingFilmTitles:
						output['filmTitles'][filmTitlesCounter] = {}
						output['filmTitles'][filmTitlesCounter]['fk_usedBy'] = []
						output['filmTitles'][filmTitlesCounter]['filmTitleValue'] = theName
						output['filmTitles'][filmTitlesCounter]['fk_usedBy'].append(row['event ID'])
						existingFilmTitles[theName] = filmTitlesCounter
						output['recordings'][recordingID]['filmTitles'].append(str(filmTitlesCounter))
						filmTitlesCounter += 1
					else:
						theFilmID = existingFilmTitles[theName]
						output['recordings'][recordingID]['filmTitles'].append(str(theFilmID))
						output['filmTitles'][theFilmID]['fk_usedBy'].append(row['event ID'])

# print(output)
with open('data_files/combined-audio-data-cleaned2.json','w+') as f:
	json.dump(output, f)
