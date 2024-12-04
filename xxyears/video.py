from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from xxyears.auth import login_required
import json
import glob
from ftplib import FTP

with open('json/.ftp_credentials.json') as file:
        credentials = json.load(file)
        
password = credentials['password']   
username = credentials['username']   
server = credentials['server']   
ftp = FTP(server)
ftp.login(user=username, passwd=password)
    
ftp_path = 'www.nanowar.it/XX_YEARS_OF_STEEL/FULL_VIDEO/'
http_path = 'http://www.nanowar.it/XX_YEARS_OF_STEEL/FULL_VIDEO/'

# Change to the specified directory
ftp.cwd(ftp_path)

files = ftp.nlst()
mp4_files = [file for file in sorted(files) if file.endswith('.mp4')]

urls = []

if mp4_files:
    for file in mp4_files:
        urls.append(http_path + file)           

bp = Blueprint('video', __name__, url_prefix='/video')

@bp.route('/play', methods=('GET', 'POST'))
@login_required
def play():
    return render_template('video/videoplayer.html', url1=urls[0], url2=urls[1], url3=urls[2]);

