import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash
try:
    from xxyears.db import get_db
    import xxyears.codes
except:
    from db import get_db
    import codes

import pickle as pkl
import pandas as pd

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        code = request.form['code']
        db = get_db()
        error = None
        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not code:
            error = 'Code is required.'

        if not codes.is_code_valid(code):
            error = 'Wrong code given.'
        else:
            codes.remove_code_from_list(code)

        if error is None:
            try:
                db.execute(
                    "INSERT INTO user (username, password, code) VALUES (?, ?, ?)",
                    (username, generate_password_hash(password), code),
                )
                db.commit()
            except db.IntegrityError:
                error = f"User {username} or code {code} is already registered. Try registering with a different code or username."
            else:
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    session['logged_in'] = False

    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM user WHERE username = ?', (username,)
        ).fetchone()

        if user is None:
            error = 'Incorrect username.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            session['logged_in'] = True
            return redirect(url_for('video.play'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/logout')
def logout():
    
    if session['logged_in']:
        flash('Logged out succesfully.')
        session.clear()
    else:
        flash('Logging out without loggin in first does not make much sense')

    return redirect(url_for('auth.login'))


def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if session['logged_in']: # in session:
            print("Login successful!")
        else:
            flash("You need to login first")
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

if __name__ == '__main__':

    test_code = 'legacy-uranus-rhapsody-4669'


