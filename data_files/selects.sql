# data sanity check on some common speakers

SELECT recordings.recordingID
FROM recordings
INNER JOIN recording_speaker as r
ON recordings.recordingID = r.recordingID
INNER JOIN speakers
ON speakers.speakerID = r.speakerID
WHERE speakers.speakerValue LIKE '%Everson%';

SELECT recordings.recordingID
FROM recordings
INNER JOIN recording_speaker as r
ON recordings.recordingID = r.recordingID
INNER JOIN speakers
ON speakers.speakerID = r.speakerID
WHERE speakers.speakerValue = 'Yvette Biro';

SELECT recordings.recordingID
FROM recordings
INNER JOIN recording_speaker as r
ON recordings.recordingID = r.recordingID
INNER JOIN speakers
ON speakers.speakerID = r.speakerID
WHERE speakers.speakerValue = 'David Thomson';
