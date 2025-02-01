from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload
from google_auth_oauthlib.flow import InstalledAppFlow

# Authenticate and build the YouTube API client
scopes = ["https://www.googleapis.com/auth/youtube.upload"]
flow = InstalledAppFlow.from_client_secrets_file("../client_secret.json", scopes)
credentials = flow.run_local_server(port=0)
youtube = build("youtube", "v3", credentials=credentials)

youtube.videos().update(
    part="status",
    body={
        "id": "KfLxaZNSf2k",
        "status": {
            "privacyStatus": "private",
            "allowed": ["nanowarVEVO@gmail.com", "ecarlesi83@gmail.com"]
        }
    }
).execute()
