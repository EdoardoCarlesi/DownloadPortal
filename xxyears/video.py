from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from xxyears.auth import login_required
import json


file_path = 'json/video_filenames.json'

with open(file_path) as file:
    filenames = json.load(file)

bp = Blueprint('video', __name__, url_prefix='/video')

fname1 = filenames['filename1']
fname2 = filenames['filename2']
fname3 = filenames['filename3']

fformat = 'png'
#fformat = 'mp4'

url1 = f'http:////www.nanowar.it/XX_YEARS_OF_STEEL/{fname1}.{fformat}'
url2 = f'http:////www.nanowar.it/XX_YEARS_OF_STEEL/{fname2}.{fformat}'
url3 = f'http:////www.nanowar.it/XX_YEARS_OF_STEEL/{fname3}.{fformat}'

@bp.route('/play', methods=('GET', 'POST'))
@login_required
def play():
    return render_template('video/videoplayer.html', url1=url1, url2=url2, url3=url3);

