"Google Developers Console - https://console.developers.google.com/"
"Google API Python Client - https://github.com/googleapis/google-api-python-client"
"YouTube API - https://developers.google.com/youtube/v3"

from googleapiclient.discovery import build

api_key = "yourapikeyhere"

youtube = build('youtube', 'v3', developerKey=api_key)

playlist_id = "PLMBTl5yXyrGQ68Ny1mXCAaSwbjpcVwm49"

videos = []

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
        part='statistics',
        id=','.join(vid_ids)
    )

    vid_response = vid_request.execute()

    for item in vid_response['items']:
        vid_views = item['statistics']['viewCount']

        vid_id = item['id']
        yt_link = f'https://youtu.be/{vid_id}'

        videos.append(
            {
                'views': int(vid_views),
                'url': yt_link
            }
        )

    # if there are no more pages, this returns None and breaks the loop
    nextPageToken = pl_response.get('nextPageToken')
    if not nextPageToken:
        break

videos.sort(key=lambda vid: vid['views'], reverse=True)

for video in videos[:10]:
    print(video['url'], video['views'])

