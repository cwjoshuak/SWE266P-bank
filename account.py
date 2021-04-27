from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort

from flaskr.auth import login_required
from flaskr.db import get_db

bp = Blueprint('account', __name__)

@bp.route('/')
def index():
    db = get_db()
    accounts = db.execute(
        'SELECT b.id, userAccount_id, username, amount'
        ' FROM bankAccount b JOIN userAccount u ON b.userAccount_id = u.id'
        ' WHERE userAccount_id = ?',(g.user['id'],)
    ).fetchall()
    return render_template('account/index.html', accounts=accounts)


@bp.route('/create', methods=('GET', 'POST'))
@login_required
def create():
    if request.method == 'POST':
        init_amount = request.form['amount']
        error = None

        if not init_amount:
            error = 'Initial amount required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'INSERT INTO bankAccount (amount, userAccount_id)'
                ' VALUES (?, ?)',
                (init_amount, g.user['id'])
            )
            db.commit()
            return redirect(url_for('account.index'))

    return render_template('account/create.html')

def get_account(id, check_author=True):
    account = get_db().execute(
        'SELECT b.id, userAccount_id, username, amount'
        ' FROM bankAccount b JOIN userAccount u ON b.userAccount_id = u.id'
        ' WHERE b.id = ?',
        (id,)
    ).fetchone()

    if account is None:
        abort(404, "Account id {0} doesn't exist.".format(id))

    if check_author and account['userAccount_id'] != g.user['id']:
        abort(403)

    return account

@bp.route('/<int:id>/update', methods=('GET', 'POST'))
@login_required
def update(id):
    account = get_account(id)

    if request.method == 'POST':
        amount = request.form['amount']
        error = None

        if not amount:
            error = 'Amount is required.'

        if error is not None:
            flash(error)
        else:
            db = get_db()
            db.execute(
                'UPDATE bankAccount SET amount = ?'
                ' WHERE id = ?',
                (amount, id)
            )
            db.commit()
            return redirect(url_for('account.index'))

    return render_template('account/update.html', account=account)

@bp.route('/<int:id>/delete', methods=('POST',))
@login_required
def delete(id):
    get_post(id)
    db = get_db()
    db.execute('DELETE FROM bankAccount WHERE id = ?', (id,))
    db.commit()
    return redirect(url_for('account.index'))
