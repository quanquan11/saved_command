import sqlite3
import os
from flask import g

# Define the database path
DATABASE = os.environ.get('DATABASE', 'commands.db')

def get_db():
    """
    Establishes a connection to the SQLite database.
    If the connection does not already exist, it creates one.
    """
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = sqlite3.Row  # This allows us to return rows as dictionaries
    return db

def close_connection(exception=None):
    """
    Closes the connection to the database when the application context ends.
    """
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def init_db(app):
    """
    Initializes the database by creating tables for users, categories, and commands if they do not exist.
    Populates the categories table with pre-defined command types (TSUMS, FRPT, FDAT95).
    Registers the close_connection function to be called at the end of each request.
    """
    with app.app_context():
        db = get_db()

        # Create 'users' table
        db.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            email TEXT NOT NULL
        );
        ''')

        # Create 'categories' table
        db.execute('''
        CREATE TABLE IF NOT EXISTS categories (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT UNIQUE NOT NULL
        );
        ''')

        # Create 'user_commands' table
        db.execute('''
        CREATE TABLE IF NOT EXISTS user_commands (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            command_name TEXT NOT NULL,
            command_text TEXT NOT NULL,
            command_description TEXT,
            category_id INTEGER NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (user_id) REFERENCES users(id),
            FOREIGN KEY (category_id) REFERENCES categories(id)
        );
        ''')

        # Insert default categories for TSUMS, FRPT, and FDAT95
        db.execute('''
        INSERT OR IGNORE INTO categories (id, name)
        VALUES
            (1, "TSUMS"),
            (2, "FRPT"),
            (3, "FDAT95");
        ''')

        db.commit()

    # Register close_connection to be called after each request
    app.teardown_appcontext(close_connection)

def add_user(username, password, email):
    """
    Adds a new user to the 'users' table.
    """
    db = get_db()
    try:
        db.execute('INSERT INTO users (username, password, email) VALUES (?, ?, ?)', (username, password, email))
        db.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return False
    return True

def get_user_by_username(username):
    """
    Fetches a user's details by their username.
    """
    db = get_db()
    try:
        cur = db.execute('SELECT id, username, password, email FROM users WHERE username = ?', (username,))
        user = cur.fetchone()
        return {'id': user['id'], 'username': user['username'], 'password': user['password'], 'email': user['email']} if user else None
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return None

def add_command(user_id, command_name, command_text, command_description, category_id):
    """
    Adds a new command to the 'user_commands' table with its category and user ID.
    """
    db = get_db()
    try:
        db.execute('''
            INSERT INTO user_commands (user_id, command_name, command_text, command_description, category_id) 
            VALUES (?, ?, ?, ?, ?)
        ''', (user_id, command_name, command_text, command_description, category_id))
        db.commit()
    except sqlite3.Error as e:
        print(f"Database error: {e}")

def get_commands_by_user_id(user_id, category_id=None):
    """
    Fetches commands for a specific user by user ID.
    Optionally filters by category ID.
    """
    db = get_db()
    try:
        if category_id:
            cur = db.execute('''
                SELECT command_name, command_text, command_description, created_at 
                FROM user_commands 
                WHERE user_id = ? AND category_id = ? 
                ORDER BY created_at DESC
            ''', (user_id, category_id))
        else:
            cur = db.execute('''
                SELECT command_name, command_text, command_description, created_at 
                FROM user_commands 
                WHERE user_id = ? 
                ORDER BY created_at DESC
            ''', (user_id,))
        return cur.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []

def search_commands_by_name(user_id, query, category_id):
    """
    Searches commands by their name using a search query.
    Only returns commands that belong to a specific user and category.
    """
    db = get_db()
    search_query = f'%{query}%'
    try:
        cur = db.execute('''
            SELECT command_name, command_text, command_description, created_at 
            FROM user_commands 
            WHERE user_id = ? AND category_id = ? AND command_name LIKE ? 
            ORDER BY created_at DESC
        ''', (user_id, category_id, search_query))
        return cur.fetchall()
    except sqlite3.Error as e:
        print(f"Database error: {e}")
        return []
