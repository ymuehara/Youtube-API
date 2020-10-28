"Google Developers Console - https://console.developers.google.com/"
"Google API Python Client - https://github.com/googleapis/google-api-python-client"
"YouTube API - https://developers.google.com/youtube/v3"

import re
from datetime import timedelta
from googleapiclient.discovery import build

api_key = "yourapikeyhere"

youtube = build('youtube', 'v3', developerKey=api_key)

hours_pattern = re.compile(r'(\d+)H')
minutes_pattern = re.compile(r'(\d+)M')
seconds_pattern = re.compile(r'(\d+)S')

total_seconds = 0

playlist_id = "PLMBTl5yXyrGQ68Ny1mXCAaSwbjpcVwm49"

nextPageToken = None
while True:
    pl_request = youtube.playlistItems().list(
        part='contentDetails',
        playlistId=playlist_id,
        maxResults=50,
        pageToken=nextPageToken
    )

    pl_response = pl_request.execute()

    vid_ids = []
    for item in pl_response['items']:
        vid_ids.append(item['contentDetails']['videoId'])

    vid_request = youtube.videos().list(
        part='contentDetails',
        id=','.join(vid_ids)
    )

    vid_response = vid_request.execute()

    for item in vid_response['items']:
        duration = item['contentDetails']['duration']

        hours = hours_pattern.search(duration)
        minutes = minutes_pattern.search(duration)
        seconds = seconds_pattern.search(duration)

        hours = int(minutes.group(1)) if hours else 0
        # if valor diferente de none, se for none entao 0
        minutes = int(minutes.group(1)) if minutes else 0
        seconds = int(seconds.group(1)) if seconds else 0

        video_seconds = timedelta(
            hours=hours,
            minutes=minutes,
            seconds=seconds,
        ).total_seconds()

        # print(hours, minutes, seconds, '\n')
        # print(video_seconds)

        total_seconds += video_seconds

    # if there are no more pages, this returns None and breaks the loop
    nextPageToken = pl_response.get('nextPageToken')
    if not nextPageToken:
        break

total_seconds = int(total_seconds)

minutes, seconds = divmod(total_seconds, 60)

print(f'{hours}:{minutes}:{seconds}')