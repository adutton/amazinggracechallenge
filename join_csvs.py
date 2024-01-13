import csv
import glob
import json
import os
import requests

from datetime import datetime, date, timezone
from calendar import monthrange
from pprint import pprint, pformat

HASHTAG = 'Amazing Grace'
RESULTS_FOLDER = 'results'
HASHTAG_FOLDER = os.path.join(os.path.abspath(RESULTS_FOLDER), HASHTAG.replace('#', ''))
RESULTS_FILE = os.path.join(RESULTS_FOLDER, 'deduplicated_results.csv')


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

    csv_filenames = sorted(glob.glob(os.path.join(HASHTAG_FOLDER, '*.csv')))

    print(f"Found {len(csv_filenames)} filenames")

    recording_records = dict()
    header_line = None
    total_records = 0

    for filename in csv_filenames:
        print(f"Processing {filename}")

        with open(filename, "r", encoding="utf-8") as fp:
            data_read = fp.readlines()

        total_records += len(data_read) - 1
        print(f"Found {len(data_read) - 1} rows of data")

        header_line = data_read[0]
        for data in data_read[1:]:
            recording_records.update({data.split(',', 1)[0]: data})

    print(f"Processed {total_records} rows of data total, {len(recording_records)} unique values")

    # Sort by publish date (index 7)
    reader = sorted(csv.reader(recording_records.values()), key=lambda x: x[7])

    header_row = header_line[:-1].split(',')
    print(header_line)
    print(header_row)

    print(f"Writing to {RESULTS_FILE}")
    with open(RESULTS_FILE, "w", encoding="utf-8") as results_file:
        csv_writer = csv.writer(results_file, lineterminator='\n')
        csv_writer.writerow(header_row)
        csv_writer.writerows(reader)
        #

        # results_file.writelines(sorted(reader, key=lambda x: x[7]))


if __name__ == '__main__':
    main()
