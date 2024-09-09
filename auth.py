from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from db import get_user_by_username, add_user
from flask import session, redirect, url_for, flash
from functools import wraps

ph = PasswordHasher()

# Hash a password using Argon2
def hash_password(password):
    return ph.hash(password)

# Verify a password using Argon2
def verify_password(stored_password, provided_password):
    try:
        return ph.verify(stored_password, provided_password)
    except VerifyMismatchError:
        return False

# Check if a username is already taken
def is_username_taken(username):
    user = get_user_by_username(username)
    return user is not None

# Register a new user
def register_user(username, password, email):
    if is_username_taken(username):
        return False
    hashed_password = hash_password(password)
    add_user(username, hashed_password, email)
    return True
