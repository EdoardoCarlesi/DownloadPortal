import json
from ftplib import FTP

from flask import (
    Blueprint, render_template
)

from xxyears.auth import login_required

bp = Blueprint('video', __name__, url_prefix='/video')


def ftp_connect(credentials_file_path):
    """Establish an FTP connection using credentials from a JSON file."""
    with open(credentials_file_path) as file:
        credentials = json.load(file)

    server = credentials['server']
    username = credentials['username']
    password = credentials['password']

    ftp = FTP(server)
    ftp.login(user=username, passwd=password)
    return ftp


@bp.route('/play', methods=('GET', 'POST'))
@login_required
def play():
    credentials_file = 'json/.ftp_credentials.json'
    ftp = ftp_connect(credentials_file)

    ftp_path = 'www.nanowar.it/XX_YEARS_OF_STEEL/FULL_VIDEO/'
    http_path = 'https://www.nanowar.it/XX_YEARS_OF_STEEL/FULL_VIDEO/'

    # Change to the specified directory
    ftp.cwd(ftp_path)

    files = ftp.nlst()
    mp4_files = [file for file in sorted(files) if file.endswith('.mp4')]

    urls = []

    if mp4_files:
        for file in mp4_files:
            urls.append(http_path + file)

    return render_template('video/videoplayer.html', url1=urls[0], url2=urls[1], url3=urls[2])
