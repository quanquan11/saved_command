from flask import session, redirect, url_for, flash
from functools import wraps
import logging

def login_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            flash('Please log in to access this page.', 'warning')
            return redirect(url_for('login'))
        return func(*args, **kwargs)
    return decorated_function

def set_session(user_id, username, email, remember_me=False):
    session['user_id'] = user_id
    session['username'] = username
    session['email'] = email
    session.permanent = remember_me
    print(f"Session set: user_id={user_id}, username={username}, email={email}")