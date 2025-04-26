from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
import os
import pickle

# Set up the API client
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]
API_SERVICE_NAME = 'youtube'
API_VERSION = 'v3'

def get_sub_count(channel_id=None):
    # Authenticate using OAuth 2.0
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)
    
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        
        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)
    
    youtube = build(API_SERVICE_NAME, API_VERSION, credentials=creds)

    if channel_id:
        # Fetch subscriber count for a specific channel ID
        request = youtube.channels().list(
            part="statistics",
            id=channel_id  # Use the specified channel ID
        )
    else:
        # Fetch the authenticated user's default channel
        request = youtube.channels().list(
            part="statistics",
            mine=True
        )
    
    response = request.execute()

    # Get subscriber count
    subscriber_count = response['items'][0]['statistics']['subscriberCount']
    return subscriber_count

# Call the function with the specific channel ID you want
channel_id = "UC7pCcWylxb8DlbDNxJbkUlw"  # Replace this with the actual channel ID
subs = get_sub_count(channel_id)
print(f"Subscriber count: {subs}")
