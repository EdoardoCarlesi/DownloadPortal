import functools
from flask import Blueprint, flash, g, redirect, render_template, request, session, url_for, Flask
from werkzeug.security import check_password_hash, generate_password_hash
import secrets
from datetime import datetime, timedelta
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

try:
    from xxyears.db import get_db
    import xxyears.codes as codes
except:
    from db import get_db
    import codes

import pickle as pkl
import pandas as pd

bp = Blueprint('auth', __name__, url_prefix='/auth')
app = Flask(__name__)

@bp.route('/register', methods=('GET', 'POST'))
def register():

    print(codes.draw_random_code())

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        code = request.form['code']
        db = get_db()
        error = None

        if not email:
            error = 'Email is required.'
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
                    "INSERT INTO user (email, password, code) VALUES (?, ?, ?)",
                    (email, generate_password_hash(password), code),
                )
                db.commit()
            except db.IntegrityError:
                error = f"Code {code} or email {email} is already registered. Try registering with a different code or email."
            else:
                flash('Registration successful. You can now login.')
                return redirect(url_for("auth.login"))

        flash(error)

    return render_template('auth/register.html')


@bp.route('/login', methods=('GET', 'POST'))
def login():
    session['logged_in'] = False

    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        mail = db.execute(
            'SELECT * FROM user WHERE email = ?', (email,)
        ).fetchone()

        if mail is None:
            error = 'Incorrect email.'
        elif not check_password_hash(mail['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = email
            session['logged_in'] = True
            flash('You logged in successfully')
            return redirect(url_for('auth.user'))

        flash(error)

    return render_template('auth/login.html')


@bp.route('/user')
def user():
    db = get_db()
    user_email = session.get('user_id')
    
    if user_email:
        user = db.execute(
            'SELECT * FROM user WHERE email = ?', (user_email,)
        ).fetchone()
        
        if user:
            return render_template('auth/user.html', user=user)
    
    flash('User not found or not logged in.')
    return redirect(url_for('auth.login'))


@bp.route('/reset_password', methods=('GET', 'POST'))
def reset_password():
    if request.method == 'POST':
        email = request.form['email']
        db = get_db()
        error = None

        if not email:
            error = 'Email is required.'
        else:
            user = db.execute(
                'SELECT * FROM user WHERE email = ?', (email,)
            ).fetchone()
            if user is None:
                error = 'No account with that email address.'

        if error is None:
            # Generate a unique token
            token = secrets.token_urlsafe(32)
            expiration = datetime.now() + timedelta(hours=1)
            print(email, token, expiration)
            # Store the token in the database
            db.execute(
                'INSERT INTO password_reset (email, token, expiration) VALUES (?, ?, ?)',
                (email, token, expiration)
            )
            db.commit()

            # Generate the reset link
            reset_link = url_for('auth.reset_password_confirm', token=token, _external=True)

            # Send email with reset link
            smtp_server = 'smtp.xxyearsofsteel.com'
            smtp_port = 587
            smtp_username = os.environ.get('SMTP_USERNAME')
            smtp_password = os.environ.get('SMTP_PASSWORD')

            msg = MIMEMultipart()
            msg['From'] = 'password-reset@xxyearsofsteel.com'
            msg['To'] = email
            msg['Subject'] = 'Password Reset Request'
            msg.attach(MIMEText(f'Click the following link to reset your password: {reset_link}', 'plain'))

            with smtplib.SMTP(smtp_server, smtp_port) as server:
                server.starttls()
                server.login(smtp_username, smtp_password)
                server.send_message(msg)

            flash('An email has been sent with instructions to reset your password.')
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/reset_password.html')

@bp.route('/reset_password/<token>', methods=('GET', 'POST'))
def reset_password_confirm(token):
    db = get_db()
    reset_request = db.execute(
        'SELECT * FROM password_reset WHERE token = ?', (token,)
    ).fetchone()

    if reset_request is None or datetime.now() > reset_request['expiration']:
        flash('Invalid or expired reset link.')
        return redirect(url_for('auth.login'))

    if request.method == 'POST':
        new_password = request.form['new_password']
        confirm_password = request.form['confirm_password']
        error = None

        if not new_password:
            error = 'New password is required.'
        elif new_password != confirm_password:
            error = 'Passwords do not match.'

        if error is None:
            db.execute(
                'UPDATE user SET password = ? WHERE email = ?',
                (generate_password_hash(new_password), reset_request['email'])
            )
            db.execute('DELETE FROM password_reset WHERE token = ?', (token,))
            db.commit()
            flash('Your password has been reset. You can now login with your new password.')
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/reset_password_confirm.html')


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

        try:
            if session['logged_in']: # in session:
                print("Login successful!")
            else:
                flash("You need to login first")
                return redirect(url_for('auth.login'))
        except:
            flash("You need to login first")
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

if __name__ == '__main__':

    test_code = 'legacy-uranus-rhapsody-4669'


