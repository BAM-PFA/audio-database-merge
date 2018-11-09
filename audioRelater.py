#!/usr/bin/env python3

import csv
import json

output = {
	'recordings' : {
		# 'pk_recordingID' : {
		# 	'tapeNumber' : '',
		# 	'tapeSide' : '',
		# 	'month' : '',
		# 	'day' : '',
		# 	'year' : '',
		# 	'speakers' : [],
		# 	'filmTitles' : [],
		# 	'permissions' : '',
		# 	'location' : '',
		#	'recordingTitle' : '',	
		# 	'recordingNotes' : '',
		#	'recordingRecordingNotes' : ''
		# }
	},
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

speakersCounter = 1
filmTitlesCounter = 1
existingSpeakers = {}
existingFilmTitles = {}

# with open('audioZ_final.csv','r') as f:
with open('audio_combined-cleaned.csv','r') as f:
	reader = csv.DictReader(f)
	for row in reader:
		# print(row)
		# sys.exit()
		recordingID = row['event ID']
		output['recordings'][recordingID] = {}
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
					output['recordings'][recordingID]['speakers'].append(str(speakersCounter))
					if not theName in existingSpeakers:
						output['speakers'][speakersCounter] = {}
						output['speakers'][speakersCounter]['fk_usedBy'] = []
						output['speakers'][speakersCounter]['speakerValue'] = theName
						output['speakers'][speakersCounter]['fk_usedBy'].append(row['event ID'])
						existingSpeakers[theName] = speakersCounter
						speakersCounter += 1
					else:
						theSpeakerID = existingSpeakers[theName]
						output['speakers'][theSpeakerID]['fk_usedBy'].append(row['event ID'])
				elif key.startswith('film'):
					output['recordings'][recordingID]['filmTitles'].append(str(filmTitlesCounter))
					if not theName in existingFilmTitles:
						output['filmTitles'][filmTitlesCounter] = {}
						output['filmTitles'][filmTitlesCounter]['fk_usedBy'] = []
						output['filmTitles'][filmTitlesCounter]['filmTitleValue'] = theName
						output['filmTitles'][filmTitlesCounter]['fk_usedBy'].append(row['event ID'])
						existingFilmTitles[theName] = filmTitlesCounter
						filmTitlesCounter += 1
					else:
						theFilmID = existingFilmTitles[theName]
						output['filmTitles'][theFilmID]['fk_usedBy'].append(row['event ID'])

print(output)
# JSONoutput = json.loads(output)
# with open('audio.json','w+') as f:
with open('audioCombined.json','w+') as f:
	json.dump(output, f)



