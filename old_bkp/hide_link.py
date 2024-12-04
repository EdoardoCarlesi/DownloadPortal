import time
import hashlib
import base64
from flask import Flask, request, redirect, abort
import os

app = Flask(__name__)

# Secret key for token generation
SECRET_KEY = "CaneBlu"

# Mock file storage
FILE_STORAGE = {
    "example_file": "static/dark.css" #"www.nanowar.it/old/file/video/a_knight_at_the_opera/MakingOfNanowar.mov"
    #"example_file": "www.nanowar.it/old/file/video/a_knight_at_the_opera/MakingOfNanowar.mov"
}

def generate_masked_link(file_id, host="http://127.0.0.1:5000"):
    """
    Generate a masked download link for a specific file.
    :param file_id: Identifier for the file
    :param host: Base URL of the server
    :return: Masked URL as a clickable link
    """
    timestamp = str(int(time.time()))  # Current timestamp
    data = f"{file_id}:{timestamp}:{SECRET_KEY}"
    token = hashlib.sha256(data.encode()).hexdigest()
    masked_token = base64.urlsafe_b64encode(f"{file_id}:{timestamp}:{token}".encode()).decode()
    return f"{host}/download/{masked_token}"


@app.route("/download/<masked_token>")
def download(masked_token):
    """
    Endpoint to handle file downloads through masked links.
    """
    try:
        # Decode and extract token data
        decoded_data = base64.urlsafe_b64decode(masked_token).decode()
        file_id, timestamp, token = decoded_data.split(":")

        # Validate the token
        expected_token = hashlib.sha256(f"{file_id}:{timestamp}:{SECRET_KEY}".encode()).hexdigest()
        if token != expected_token:
            return abort(403, "Invalid or tampered token")

        # Ensure the file exists in our mapping
        if file_id not in FILE_STORAGE:
            return abort(404, "File not found")

        # Serve the file securely
        file_path = FILE_STORAGE[file_id]
        if not os.path.exists(file_path):
            return abort(404, "File not found on the server")

        return send_file(file_path, as_attachment=True)

    except Exception as e:
        return abort(400, f"Bad request: {str(e)}")


if __name__ == "__main__":
    # Generate a masked link for the example file
    file_id = "knight_video"  # File identifier
    host = "http://127.0.0.1:5000"  # Base server URL
    masked_url = generate_masked_link(file_id, host=host)
    print(f"Your masked download link: {masked_url}")

    # Start Flask app
    app.run(debug=True)

