import csv, os, re, fcntl, secrets
from contextlib import contextmanager
from datetime import datetime
from flask import Flask, request, render_template
from flask.sansio.blueprints import Blueprint
from xxyears import mail

CODES_FILE_ORIGINAL = 'xxyears/data/videocodes.txt'
CODES_FILE_SELL = 'xxyears/data/videocodes_sell.txt'
CODES_USED = 'xxyears/data/codes_used.csv'
CODES_LOCK = 'xxyears/data/codes.lock'

# Row status in CODES_USED:
#   RESERVED  sell code paid for, not yet redeemed (it can still be redeemed)
#   SOLD      sell code redeemed
#   REDEEMED  free (original) code redeemed
FINAL_STATUSES = ('SOLD', 'REDEEMED')

bp = Blueprint('codes', __name__, url_prefix='/')
app = Flask(__name__)

# Rejects whitespace (incl. CR/LF, to block mail header injection) and overlong input.
EMAIL_RE = re.compile(r'^[^@\s<>,;:"]+@[^@\s<>,;:"]+\.[^@\s<>,;:"]+$')


def is_valid_email(email):
    return len(email) <= 254 and EMAIL_RE.match(email) is not None


@contextmanager
def codes_lock():
    """Serializes purchases and redemptions across processes (e.g. gunicorn workers)."""
    with open(CODES_LOCK, 'a') as lock_file:
        fcntl.flock(lock_file, fcntl.LOCK_EX)
        try:
            yield
        finally:
            fcntl.flock(lock_file, fcntl.LOCK_UN)


def append_code_row(email, code, status):
    """Appends a row to CODES_USED. Raises on failure so a code is never handed out unrecorded."""
    current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    with open(CODES_USED, mode='a', newline='') as file:
        csv.writer(file).writerow([email, code, current_date, status])
    print(f'Appended {email}, {code}, {current_date}, {status} to {CODES_USED}')


@bp.route('/', methods=['GET', 'POST'])
def redeem():

    if request.method == 'POST':
        email = request.form.get('email', '').strip()
        code = request.form.get('code', '').strip()
        error = None

        if not email:
            error = 'Email is required.'
        elif not is_valid_email(email):
            error = 'Invalid email address.'
        elif not code:
            error = 'Code is required.'

        if error is None:
            with codes_lock():
                if is_code_valid(code):
                    mail.send_download_link(email, code)
                    append_code_row(email, code, 'SOLD' if is_code_sell(code) else 'REDEEMED')
                    return render_template('video/success.html', code=code, mail=email)
                print(f'Code {code} was inserted, but it did not work.')
                error = 'Wrong code given! Check the spelling or check that this has not been redeemed already'

        return render_template('video/error.html', error=error, code=code)


def read_text_list(path):
    if not os.path.exists(path):
        return []
    with open(path, encoding='utf8') as file:
        return [line.strip() for line in file if line.strip()]


def get_codes():
    if os.path.exists(CODES_FILE_ORIGINAL) and os.path.exists(CODES_FILE_SELL):
        return read_text_list(CODES_FILE_ORIGINAL), read_text_list(CODES_FILE_SELL)
    else:
        print(f"One or more files do not exist: {CODES_FILE_ORIGINAL}, {CODES_FILE_SELL}")
        return [], []


def read_code_rows():
    """Returns the [email, code, date, status] rows of CODES_USED."""
    if not os.path.exists(CODES_USED):
        return []
    with open(CODES_USED, mode='r', newline='') as file:
        return [row for row in csv.reader(file) if len(row) >= 4]


def reserve_sell_code(email):
    """
    Draws a random sell code no other buyer holds and records it as RESERVED for `email`.
    Returns None when no code is left.
    """
    with codes_lock():
        _, codes_sell = get_codes()
        taken = {row[1] for row in read_code_rows()}
        available = [code for code in codes_sell if code not in taken]
        if not available:
            return None
        code = secrets.choice(available)
        append_code_row(email, code, 'RESERVED')
        return code


def is_code_valid(code):
    codes_original, codes_sell = get_codes()
    if code not in codes_original and code not in codes_sell:
        return False
    finished = {row[1] for row in read_code_rows() if row[3] in FINAL_STATUSES}
    return code not in finished


def is_code_sell(code):
    co, cs = get_codes()
    if cs:
        if code in cs:
            return True
        else:
            return False
    else:
        print("No sell codes found.")
        return False
