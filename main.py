"Google Developers Console - https://console.developers.google.com/"
"Google API Python Client - https://github.com/googleapis/google-api-python-client"
"YouTube API - https://developers.google.com/youtube/v3"

from googleapiclient.discovery import build

api_key = ""

youtube = build('youtube', 'v3', developerKey=api_key)

request = youtube.channels().list(
    part='statistics',
    forUsername=('schafer5')
)

response = request.execute()

print(response)