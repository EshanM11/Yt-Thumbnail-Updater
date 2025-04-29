from googleapiclient.discovery import build
from google.oauth2 import service_account

SCOPES = ["https://www.googleapis.com/auth/youtube.readonly"]
CHANNEL_ID = "UC7pCcWylxb8DlbDNxJbkUlw"  # Replace with your channel ID

def get_credentials():
    creds = service_account.Credentials.from_service_account_file(
        'credentials.json', scopes=SCOPES
    )
    return creds

def get_sub_count():
    creds = get_credentials()
    youtube = build('youtube', 'v3', credentials=creds)

    request = youtube.channels().list(
        part='statistics',
        id=CHANNEL_ID
    )
    response = request.execute()

    sub_count = int(response['items'][0]['statistics']['subscriberCount'])
    return sub_count

if __name__ == "__main__":
    subs = get_sub_count()
    print(f"Subscriber count: {subs}")
