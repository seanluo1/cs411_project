import functools

from flask import (
    Blueprint, flash, g, redirect, render_template, request, session, url_for
)
from werkzeug.security import check_password_hash, generate_password_hash

from app.db import get_db

bp = Blueprint('auth', __name__, url_prefix='/auth')

@bp.route('/register', methods=('GET', 'POST'))
def register():
    if request.method == 'POST':
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None

        if not email:
            error = 'Email is required.'
        elif not password:
            error = 'Password is required.'
        elif not firstName:
            error = 'First name is required.'
        elif not lastName:
            error = 'Last name is required.'
        elif db.execute(
            'SELECT Id FROM User WHERE email = ?', (email,)
        ).fetchone() is not None:
            error = 'Email {} is already registered.'.format(email)

        if error is None:
            db.execute(
                'INSERT INTO User (FirstName, LastName, Email, Password) VALUES (?, ?, ?, ?)',
                (firstName, lastName, email, generate_password_hash(password))
            )
            db.commit()
            return redirect(url_for('auth.login'))

        flash(error)

    return render_template('auth/register.html')

@bp.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM User WHERE email = ?', (email,)
        ).fetchone()

        if user is None:
            error = 'Incorrect email.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('index'))

        flash(error)

    return render_template('auth/login.html')

@bp.route('/deleteAccount', methods=('GET', 'POST'))
def deleteAccount():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        error = None
        user = db.execute(
            'SELECT * FROM User WHERE email = ?', (email,)
        ).fetchone()

        if user is None:
            error = 'Invalid Email.'
        elif not check_password_hash(user['password'], password):
            error = 'Incorrect password.'

        if error is None:
            db.execute(
                'DELETE FROM User WHERE Email=(?)',
                (email,)
            )
            db.commit()
            return render_template('auth/deleteSuccess.html')

        flash(error)

    return render_template('auth/deleteAccount.html')

@bp.before_app_request
def load_logged_in_user():
    user_id = session.get('user_id')

    if user_id is None:
        g.user = None
    else:
        g.user = get_db().execute(
            'SELECT * FROM User WHERE Id = ?', (user_id,)
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