import json
import os
import requests

from datetime import datetime
from pprint import pprint, pformat

YOUTUBE_API_KEY = os.environ['YOUTUBE_API_KEY']
YOUTUBE_SOURCE = 'youtube'
#HASHTAG = '#amazinggracechallenge'
HASHTAG = '#antimlm'


class YouTubeFetcher:
    pass


class CaptureSession:
    def __init__(self, source_type, api_url, hashtag, date_initiated,
                 from_date, to_date, is_complete, recordings_filename,
                 capture_session_id=None):
        self.capture_session_id = capture_session_id or date_initiated.strftime('%Y-%m-%dT%H:%M:%SZ')
        self.source_type = source_type
        self.api_url = api_url
        self.hashtag = hashtag
        self.from_date = from_date
        self.to_date = to_date
        self.is_complete = is_complete
        self.recordings_filename = recordings_filename

    def __repr__(self):
        return json.dumps(vars(self), indent=4)


class RecordingRecord:
    def __init__(self, key, hashtag, recording_url, title, author, author_url, date_recorded,
                 source_type, capture_session_id,
                 length_seconds=None, verified_by=None, verified_on=None, verified_notes=None,
                 verified_does_count=None):
        self.key = key
        self.hashtag = hashtag
        self.recording_url = recording_url
        self.title = title
        self.author = author
        self.author_url = author_url
        self.length_seconds = length_seconds
        self.date_recorded = date_recorded
        self.verified_by = verified_by
        self.verified_on = verified_on
        self.verified_notes = verified_notes
        self.verified_does_count = verified_does_count
        self.source_type = source_type
        self.capture_session_id = capture_session_id

    def __repr__(self):
        return json.dumps(vars(self), indent=4)


# Load all capture session records
capture_sessions = []
# Load all recording records
recording_records = []
# Create a new capture session
capture_session = CaptureSession(
    source_type=YOUTUBE_SOURCE,
    api_url='',
    hashtag=HASHTAG,
    date_initiated=datetime.now(),
    from_date=datetime.now(),
    to_date=None,
    is_complete=False,
    recordings_filename=None)

# Determine the latest capture FromDate
# Start capturing, repeat until number of calls achieved OR no more records exist
# Call API

# '?part=snippet&order=date&publishedAfter=2023-10-01T00%3A00%3A00Z&q=%23antimlm&type=video&key=[YOUR_API_KEY]' \
#  --header 'Authorization: Bearer [YOUR_ACCESS_TOKEN]' \
#  --header 'Accept: application/json' \
#  --compressed

url = 'https://youtube.googleapis.com/youtube/v3/search'

for i in [0]:

    params = dict(
        part='snippet',
        order='date',
        publishedAfter='2023-10-01T00:00:00Z',
        q=HASHTAG,
        type='video',
        key=YOUTUBE_API_KEY,
        fields='nextPageToken,pageInfo,items/id/videoId,items/snippet(title,channelTitle,channelId,publishTime)',
    )

    headers = {
        'Accept-Encoding': 'gzip',
    }

    resp = requests.get(url=url, params=params, headers=headers)

    if resp.status_code != 200:
        print(resp.json())
        continue

    data = resp.json()

    print(json.dumps(data, indent=4))
    # pprint(data['items'][0])

    for item in data['items']:
        pprint(item)
        snippet = item['snippet']
        recording_record = RecordingRecord(
            key=item['id']['videoId'],
            hashtag=HASHTAG,
            source_type=YOUTUBE_SOURCE,
            recording_url=f"https://www.youtube.com/watch?v={item['id']['videoId']}",
            title=snippet['title'],
            author=snippet['channelTitle'],
            author_url=f"https://www.youtube.com/channel/{snippet['channelId']}",
            date_recorded=snippet['publishTime'],
            capture_session_id=capture_session.capture_session_id
        )
        print(recording_record)
# Parse data into DTOs
# Convert DTOs into recording records
# If not already stored,
# Save to recording record
# If stored but different
# Log & update the recording record
# Update capture session information
# Save data about the capture session
# Save data about the recording records
