import sqlite3
import os
from flask import g

DATABASE = os.environ.get('DATABASE', 'users.db')

def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db

def close_connection(exception=None):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db(app):
    with app.app_context():
        db = get_db()
        db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL
        );
        ''')
        db.execute('''
        CREATE TABLE IF NOT EXISTS user_commands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            command_name TEXT NOT NULL,
            command_text TEXT NOT NULL,
            command_description TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id)
        );
        ''')
        db.commit()
    app.teardown_appcontext(close_connection)

def get_user_by_username(username):
    db = get_db()
    cur = db.execute('SELECT id, username, password, email FROM users WHERE username = ?', (username,))
    user = cur.fetchone()
    return {'id': user[0], 'username': user[1], 'password': user[2], 'email': user[3]} if user else None

def add_user(username, password, email):
    db = get_db()
    db.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', (username, password, email))
    db.commit()

def add_command(user_id, command_name, command_text, command_description):
    db = get_db()
    db.execute('''
    INSERT INTO user_commands (user_id, command_name, command_text, command_description) 
    VALUES (?, ?, ?, ?)
    ''', (user_id, command_name, command_text, command_description))
    db.commit()

def get_commands_by_user_id(user_id):
    db = get_db()
    return db.execute('SELECT command_name, command_text, command_description, created_at FROM user_commands WHERE user_id = ?', (user_id,)).fetchall()

def search_commands_by_name(user_id, search_query):
    db = get_db()
    query = f"%{search_query}%"  # SQL wildcard pattern for LIKE search
    return db.execute('''
        SELECT command_name, command_text, command_description, created_at
        FROM user_commands
        WHERE user_id = ? AND command_name LIKE ?
    ''', (user_id, query)).fetchall()
