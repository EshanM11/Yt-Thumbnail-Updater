from googleapiclient.discovery import build
import pickle
import os

def upload_thumbnail(video_id, thumbnail_path):
    # Load credentials
    with open("token.pickle", "rb") as token:
        creds = pickle.load(token)

    youtube = build("youtube", "v3", credentials=creds)

    youtube.thumbnails().set(
        videoId=video_id,
        media_body=thumbnail_path
    ).execute()

    print("Thumbnail uploaded successfully!")
