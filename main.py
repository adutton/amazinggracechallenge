import csv
import json
import os
import requests

from datetime import datetime
from pprint import pprint, pformat

YOUTUBE_API_KEY = os.environ['YOUTUBE_API_KEY']
YOUTUBE_SOURCE = 'youtube'
# HASHTAG = '#amazinggracechallenge'
HASHTAG = '#antimlm'
RESULTS_FOLDER = 'results'
HASHTAG_FOLDER = os.path.join(os.path.abspath(RESULTS_FOLDER), HASHTAG.replace('#', ''))


def undo_html_encoding(value):
    return value.replace('&#39;', '\'')

class CaptureSession:
    def __init__(self, source_type, hashtag, date_initiated,
                 from_date, to_date, is_complete,
                 capture_session_id=None):
        self.capture_session_id = capture_session_id or date_initiated.strftime('%Y%m%dT%H%M%S')
        self.source_type = source_type
        self.hashtag = hashtag
        self.from_date = from_date
        self.to_date = to_date
        self.is_complete = is_complete

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


def main():

    if not os.path.isdir(HASHTAG_FOLDER):
        os.makedirs(HASHTAG_FOLDER)


    # Load all capture session records
    capture_sessions = []
    # Load all recording records
    recording_records = []
    # Create a new capture session
    capture_session = CaptureSession(
        source_type=YOUTUBE_SOURCE,
        hashtag=HASHTAG,
        date_initiated=datetime.now(),
        from_date=datetime.now(),
        to_date=None,
        is_complete=False,
    )

    # Determine the latest capture FromDate
    # Start capturing, repeat until number of calls achieved OR no more records exist
    url = 'https://youtube.googleapis.com/youtube/v3/search'

    next_page_token = ""
    max_pages_to_fetch = 3
    max_results_per_page = 50  # Maximum 50
    pages_count = 0

    while pages_count < max_pages_to_fetch and next_page_token is not None:
        print(f"fetching page {pages_count}")
        params = dict(
            part='snippet',
            order='date',
            publishedAfter='2023-11-01T00:00:00Z',
            q=HASHTAG,
            type='video',
            key=YOUTUBE_API_KEY,
            fields='nextPageToken,pageInfo,items/id/videoId,items/snippet(title,channelTitle,channelId,publishTime)',
            pageToken=next_page_token,
            maxResults=max_results_per_page,
        )

        headers = {
            'Accept-Encoding': 'gzip',
        }

        resp = requests.get(url=url, params=params, headers=headers)

        if not resp.ok:
            # TODO: Handle errors
            print(resp.json())
            continue

        data = resp.json()

        # print(json.dumps(data, indent=4))
        # pprint(data['items'][0])

        for item in data['items']:
            # Convert DTOs into recording records
            # pprint(item)
            print("fetched item")
            snippet = item['snippet']
            recording_record = RecordingRecord(
                key=item['id']['videoId'],
                hashtag=HASHTAG,
                source_type=YOUTUBE_SOURCE,
                recording_url=f"https://www.youtube.com/watch?v={item['id']['videoId']}",
                title=undo_html_encoding(snippet['title']),
                author=undo_html_encoding(snippet['channelTitle']),
                author_url=f"https://www.youtube.com/channel/{snippet['channelId']}",
                date_recorded=snippet['publishTime'],
                capture_session_id=capture_session.capture_session_id
            )

            print("appended record")
            recording_records.append(recording_record)
            # print(recording_record)

        next_page_token = data.get('nextPageToken')
        print(f"next page token: {next_page_token}")
        pages_count += 1

        # If not already stored,
            # Save to recording record
        # If stored but different
            # Log & update the recording record

    #print(recording_records)
    # Update capture session information
    # Save data about the capture session
    # Save data about the recording records

    if not recording_records:
        print('No records to save')
        exit()

    csv_file_name = os.path.join(HASHTAG_FOLDER, capture_session.capture_session_id + '.csv')
    print(f'Writing results to {csv_file_name}')
    with open(csv_file_name, 'w+', newline='') as csv_file:
        fieldnames = recording_records[0].__dict__.keys()
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)

        writer.writeheader()
        for recording_record in recording_records:
            writer.writerow(recording_record.__dict__)


if __name__ == '__main__':
    main()