import pickle as pkl
import csv
import pandas as pd
import random
from datetime import datetime
from flask import Flask, request, flash, render_template
from flask.sansio.blueprints import Blueprint
from xxyears import mail

CODES_FILE_ORIGINAL = 'xxyears/static/videocodes.pkl'
CODES_FILE_SELL = 'xxyears/static/videocodes_sell.pkl'
CODES_FILE_VALID = 'xxyears/static/valid_codes.pkl'
CODES_USED = 'xxyears/static/codes_used.csv'

bp = Blueprint('codes', __name__, url_prefix='/')
app = Flask(__name__)

def write_code_to_csv(email, code):
    """
    Writes or appends the email, code, and the current date to the CODES_USED CSV.
    """
    try:
        current_date = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        with open(CODES_USED, mode='a', newline='') as file:
            writer = csv.writer(file)
            if is_code_sell(code):
                sold_string = ('SOLD')
            else:
                sold_string = ('REDEEMED')
            writer.writerow([email, code, current_date, sold_string])
        print(f'Appended {email}, {code}, {current_date} to {CODES_USED}')
    except Exception as e:
        print(f'Failed to write to {CODES_USED}: {e}')

@bp.route('/', methods=['GET', 'POST'])
def redeem():

    if request.method == 'POST':
        email = request.form['email']
        code = request.form['code']
        error = None

        if not email:
            error = 'Email is required.'
        elif not code:
            error = 'Code is required.'

        if not is_code_valid(code):
            print(f'Code  {code} was inserted, but it did not work.')
            error = 'Wrong code given! Check the spelling or check that this has not been redeemed already'

        if error is None:
            mail.send_download_link(email, code)
            write_code_to_csv(email, code)
            return render_template('video/success.html', code=code, mail=email)
        else:
            return render_template('video/error.html', error=error, code=code)

def get_codes():

    codes_original = pkl.load(open(CODES_FILE_ORIGINAL, 'rb'))
    codes_sell = pkl.load(open(CODES_FILE_SELL, 'rb'))
    return codes_original, codes_sell

def get_used_codes():
    """
    Reads the CODES_USED CSV file and returns a list of codes.
    """
    try:
        with open(CODES_USED, mode='r') as file:
            reader = csv.reader(file)
            codes = [row[1] for row in reader if len(row) > 1]
        return codes
    except Exception as e:
        print(f"Failed to read from {CODES_USED}: {e}")
        return []


def draw_random_sell_code():

    co, cs = get_codes()
    n_cs = random.randint(0, len(cs))
    code = cs[n_cs]

    if code in get_used_codes():
        draw_random_sell_code()
    else:
        return code


def is_code_valid(code):
    
    codes_valid = pkl.load(open(CODES_FILE_VALID, 'rb'))
    codes_used = get_used_codes()

    if (code in codes_valid) and (not (code in codes_used)):
        return True
    else:
        return False


def is_code_sell(code):

    co, cs = get_codes()

    if code in cs:
        return True
    else:
        return False


def convert_pkl_to_csv():
    """
    Converts the three pkl files to csv.
    """
    codes_original = pkl.load(open(CODES_FILE_ORIGINAL, 'rb'))
    codes_sell = pkl.load(open(CODES_FILE_SELL, 'rb'))
    codes_valid = pkl.load(open(CODES_FILE_VALID, 'rb'))

    # Save each as a CSV file, assuming each code list is iterable
    pd.DataFrame({"codes": codes_original}).to_csv(CODES_FILE_ORIGINAL.replace('.pkl', '.csv'), index=False)
    pd.DataFrame({"codes": codes_sell}).to_csv(CODES_FILE_SELL.replace('.pkl', '.csv'), index=False)
    pd.DataFrame({"codes": codes_valid}).to_csv(CODES_FILE_VALID.replace('.pkl', '.csv'), index=False)

if __name__ == '__main__':

    this_code = 'houdini-requiem-ironmonger-6544'
    draw_random_sell_code()

    # Convert .pkl files to .csv
    convert_pkl_to_csv()
