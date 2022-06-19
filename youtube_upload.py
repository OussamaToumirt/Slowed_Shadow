import datetime
from Google import Create_Service  
from googleapiclient.http import MediaFileUpload
import os


dir_path = os.path.dirname(os.path.realpath(__file__))

def youtube(video_id, video_title):
    CLIENT_SECRET_FILE = 'client.json'
    API_NAME = 'youtube'
    API_VERSION = 'v3'
    SCOPES = ['https://www.googleapis.com/auth/youtube.upload']

    service = Create_Service(CLIENT_SECRET_FILE, API_NAME, API_VERSION, SCOPES)

    upload_date_time = datetime.datetime(2020, 12, 25, 12, 30, 0).isoformat() + '.000Z'



    request_body = {
        'snippet': {
            'categoryI': 19,
            'title': video_title,
            'description': 'Please Don\'t forget subscribe to my channel',
            'tags': ['Slowed', 'Reverb', 'slowed and reverbed', 'reverb', 'slowed and reverb'],
        },
        'status': {
            'privacyStatus': 'private',
            'publishAt': upload_date_time,
            'selfDeclaredMadeForKids': False, 
        },
        'notifySubscribers': False
    }

    mediaFile = MediaFileUpload(dir_path + '/ready_to_upload/' + video_id + '.mp4')

    response_upload = service.videos().insert(
        part='snippet,status',
        body=request_body,
        media_body=mediaFile
    ).execute()


    service.thumbnails().set(
        videoId=response_upload.get('id'),
        media_body=MediaFileUpload(dir_path + '/thumbnails/' + f'thumb-{video_id}' + '.jpg')
    ).execute()