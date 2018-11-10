# recordings
SELECT 'recordingID','recordingPictionID','recordingFilename','recordingPermissions','recordingDate','recordingDay','recordingMonth','recordingYear','recordingLocation','recordingPFASeries','recordingEventTitle','recordingEventNotes','recordingEventRecordingNotes','recordingTapeNumber','recordingTapeSide','recordingDigitizer','recordingFileSize'
UNION ALL
SELECT recordingID, recordingPictionID, recordingFilename, recordingPermissions, recordingDate, recordingDay, recordingMonth, recordingYear, recordingLocation, recordingPFASeries, recordingEventTitle, recordingEventNotes, recordingEventRecordingNotes, recordingTapeNumber, recordingTapeSide, recordingDigitizer, recordingFileSize
FROM recordings
INTO OUTFILE '/Users/michael/recordings.csv';

# filmTitles
SELECT 'filmTitleID','filmTitleValue'
UNION ALL
SELECT filmTitleID, filmTitleValue
FROM filmTitles
INTO OUTFILE '/Users/michael/filmTitles.csv';

# speakers
SELECT 'speakerID','speakerValue'
UNION ALL
SELECT speakerID, speakerValue
FROM speakers
INTO OUTFILE '/Users/michael/speakers.csv'
FIELDS ENCLOSED BY '"';

# recordingDigitalStatus
SELECT 'recordingDigitalStatusID','recordingDigitalStatusValue'
UNION ALL
SELECT recordingDigitalStatusID, recordingDigitalStatusValue
FROM recordingDigitalStatus
INTO OUTFILE '/Users/michael/recordingDigitalStatus.csv';

# recording_film join table
SELECT 'recordingID','filmTitleID'
UNION ALL
SELECT recordingID, filmTitleID
FROM recording_film
INTO OUTFILE '/Users/michael/recording_film.csv';

# recording_speaker join table
SELECT 'recordingID','speakerID'
UNION ALL
SELECT recordingID, speakerID
FROM recording_speaker
INTO OUTFILE '/Users/michael/recording_speaker.csv';

# recording_digiStatus join table
SELECT 'recordingID','recordingDigitalStatusID'
UNION ALL
SELECT recordingID, recordingDigitalStatusID
FROM recording_digiStatus
INTO OUTFILE '/Users/michael/recording_digiStatus.csv';
