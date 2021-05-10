import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

import re
import sys

bp = Blueprint('auth', __name__)
@bp.route('/register-1', methods=(['GET', 'POST']))
def register1():
    if request.method == 'POST':
        username = request.form['username']
        return redirect(url_for('auth.register2', username=username))
    return render_template('auth/register1.html')

@bp.route('/register-2', methods=(['GET', 'POST']))
def register2():
    username = request.args.get('username', '')
    if request.method == 'POST':

        password = request.form['password']
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        phonenumber = request.form['phonenumber']
        initamount = request.form['initamount']
        db = get_db()
        error = None

        if not username:
            error = 'Username is required.'
        elif not password:
            error = 'Password is required.'
        elif not firstname:
            error = 'First name required.'
        elif not lastname:
            error = 'Last name required.'
        elif phonenumber.isnumeric() == False:
            error = 'Phone number not numeric'
        elif not initamount:
            error = 'Initial amount required.'
        elif verify_number(initamount) == False:
            error = 'Not a valid numeric input'
        elif db.execute(
                'SELECT id FROM userAccount WHERE username = ?', (username,)
        ).fetchone() is not None:
            error = 'User {} is already registered.'.format(username)

        if len(username) > 127:
            error = "Username too long"
        elif len(password) > 127:
            error = "Password too long"

        pat = re.compile("[_\\-\\.0-9a-z]+")
        usernameRegex = pat.fullmatch(username)
        if usernameRegex is None:
            error = "Username contains illegal characters"
        passwordRegex = pat.fullmatch(password)
        if passwordRegex is None:
            error = "Password contains illegal characters"

        if error is None:
            db.execute(
                'INSERT INTO userAccount (username, password, phoneNumber, firstName, lastName)'
                ' VALUES (?, ?, ?, ?, ?)',
                (username, generate_password_hash(password), phonenumber, firstname, lastname)
            )
            db.commit()
            userAccountInfo = db.execute(
                'SELECT id FROM userAccount WHERE username = ?', (username,)
            ).fetchone()
            userAccountId = userAccountInfo['id']
            db.execute(
                'INSERT INTO bankAccount (amount, userAccount_id)'
                ' VALUES (?, ?)',
                (initamount, userAccountId)
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)
        return render_template('auth/login.html')
    session['username'] = username
    return render_template('auth/register.html', username=username)

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        target = request.args.get('target')
        if target is not None:
            return redirect(target)
        username = request.form['username']
        password = request.form['password']
        db = get_db()

        error = None
        user = None
        passwordHash = db.execute('SELECT password from userAccount WHERE username="' + username +'"').fetchone()
        if passwordHash is not None:
            statement = 'SELECT * FROM userAccount WHERE username = "' + username + '" AND ' + \
                    ('1' if check_password_hash(passwordHash['password'], password) else '0')

            user = db.execute(statement).fetchone()

        if user is None or passwordHash is None:
            error = 'Incorrect username.'
        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))
        flash(error)
    if request.method == 'GET':
        username = session.get('username', None)

        if username:
            query = 'SELECT id from userAccount WHERE username="' + username + '"'
            db = get_db()
            user_id = db.execute(query).fetchone()

            if(user_id['id']):
                session['user_id'] = user_id['id']
                return redirect(url_for('index'))
    return render_template('auth/login.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')
    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM userAccount WHERE id = ?', (user_id,)
        ).fetchone()

@bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('index'))

# def login_required(view):
#     @functools.wraps(view)
#     def wrapped_view(**kwargs):
#         if g.user is None:
#             return redirect(url_for('auth.login'))
#
#         return view(**kwargs)
#
#     return wrapped_view

def verify_number(amount):
    pattern = re.compile('(0|[1-9][0-9]*)(\\.[0-9]{2})?')
    match = pattern.fullmatch(amount)
    if match is None:
        return False
    else:
        return True
