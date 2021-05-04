import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from flaskr.db import get_db

import re

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        firstname  = request.form['firstname']
        lastname = request.form['lastname']
        phonenumber = request.form['phonenumber']
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
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

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

def login_required(view):
    @functools.wraps(view)
    def wrapped_view(**kwargs):
        if g.user is None:
            return redirect(url_for('auth.login'))

        return view(**kwargs)

    return wrapped_view

