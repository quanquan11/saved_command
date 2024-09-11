from argon2 import PasswordHasher
from argon2.exceptions import VerifyMismatchError
from db import get_user_by_username, add_user
from flask import session, redirect, url_for, flash
from functools import wraps

# Initialize the password hasher
ph = PasswordHasher()

# Hash a password using Argon2
def hash_password(password):
    """
    Hashes a password using Argon2.
    Returns the hashed password as a string.
    """
    return ph.hash(password)

# Verify a password using Argon2
def verify_password(stored_password, provided_password):
    """
    Verifies the provided password against the stored hashed password.
    Returns True if the password is correct, otherwise False.
    """
    try:
        return ph.verify(stored_password, provided_password)
    except VerifyMismatchError:
        return False

# Check if a username is already taken
def is_username_taken(username):
    """
    Checks if a username is already registered in the database.
    Returns True if the username is taken, otherwise False.
    """
    user = get_user_by_username(username)
    return user is not None

# Register a new user
def register_user(username, password, email):
    """
    Registers a new user with a hashed password.
    Returns True if registration was successful, otherwise False.
    """
    if is_username_taken(username):
        return False
    hashed_password = hash_password(password)
    add_user(username, hashed_password, email)
    return True
