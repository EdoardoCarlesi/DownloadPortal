from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from xxyears.auth import login_required

bp = Blueprint('video', __name__, url_prefix='/video')

url360 = 'http:////www.nanowar.it/XX_YEARS_OF_STEEL/disco_metal.mp4'
url480 = 'http:////www.nanowar.it/XX_YEARS_OF_STEEL/disco_metal.mp4'
url720 = 'http:////www.nanowar.it/XX_YEARS_OF_STEEL/disco_metal.mp4'

@bp.route('/play', methods=('GET', 'POST'))
@login_required
def play():
    return render_template('video/videoplayer.html', url360=url360, url480=url480, url720=url720);

