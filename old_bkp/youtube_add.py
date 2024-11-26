from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import pickle
import os

# Scopes for accessing YouTube Data API
SCOPES = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def authorize_youtube():
    """Authorize and return the YouTube API client."""
    credentials = None
    # Check for existing credentials
    if os.path.exists("token.pickle"):
        with open("token.pickle", "rb") as token:
            credentials = pickle.load(token)
    # If no valid credentials are available, log in
    if not credentials or not credentials.valid:
        if credentials and credentials.expired and credentials.refresh_token:
            credentials.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                "../client_secret.json", SCOPES
            )
            credentials = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.pickle", "wb") as token:
            pickle.dump(credentials, token)

    return build("youtube", "v3", credentials=credentials)

def add_email_to_private_video(video_id, email):
    """
    Adds an email to the allowed viewers of a YouTube private video.

    Args:
        video_id (str): The ID of the private video.
        email (str): The email to grant viewing access.

    Returns:
        dict: The response from the YouTube Data API.
    """
    youtube = authorize_youtube()

    try:
        # Retrieve the video details
        request = youtube.videos().list(part="recipients", id=video_id)
        response = request.execute()

        if not response["items"]:
            raise ValueError(f"Video with ID {video_id} not found.")

        # Extract existing allowed emails
        allowed_emails = response["items"][0]["status"].get("recipients", [])
        print(response["items"])
        print(allowed_emails)
        
        if email in allowed_emails:
            return {"message": "Email already has access."}

        # Add the new email
        allowed_emails.append(email)
        print(allowed_emails)

        # Update the video status with the new allowed emails
        update_request = youtube.videos().update(
            part="status",
            body={
                "id": video_id,
                "status": {
                    "privacyStatus": "private",
                    "recipients": allowed_emails
                }
            }
        )
        update_response = update_request.execute()
        print(update_response)
        
        return update_response

    except HttpError as e:
        print(f"An error occurred: {e}")
        return None


if __name__ == '__main__':

    video_id = 'stINXUd_rl8'
    email = 'ecarlesi83@gmail.com'
    #email = 'gatto@nanowar.it'

    response = add_email_to_private_video(video_id, email)
    print(response)
