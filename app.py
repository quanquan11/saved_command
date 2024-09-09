import os
import re
import logging
from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from flask_session import Session
from db import init_db, get_user_by_username, add_user, get_commands_by_user_id, add_command, search_commands_by_name
from auth import verify_password, hash_password, is_username_taken
from utils import login_required, set_session

# Initialize logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

# Log levels (sample log entries)
logging.debug("This is a debug message")  # Level 10
logging.info("This is an info message")   # Level 20
logging.warning("This is a warning message") # Level 30
logging.error("This is an error message") # Level 40
logging.critical("This is a critical message") # Level 50

# Initialize Flask app
app = Flask(__name__)

# Secret key for session management (recommended to store in environment variables)
app.secret_key = os.environ.get('SECRET_KEY', '64286b7cf51cdd4465f7a95224d82570eba648a8fb4a724e5e0efe3815fa66fb')

# Flask-Session Configuration
app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'  # Store session on filesystem
Session(app)

# Initialize the database
init_db(app)

@app.route('/')
@login_required
def index():
    logging.info(f'User data: {session}')
    return render_template('index.html', username=session.get('username'))

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out.', 'info')
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')

    username = request.form.get('username')
    password = request.form.get('password')

    user = get_user_by_username(username)
    if not user:
        flash('Username does not exist.', 'danger')
        return render_template('login.html')

    if not verify_password(user['password'], password):
        flash('Incorrect password.', 'danger')
        return render_template('login.html')

    # Set session data
    set_session(user_id=user['id'], username=user['username'], email=user['email'], remember_me='remember-me' in request.form)
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')

    username = request.form.get('username')
    password = request.form.get('password')
    confirm_password = request.form.get('confirm-password')
    email = request.form.get('email')

    # Validate input
    if not re.match(r'^(?=.*[A-Za-z])(?=.*\d)[A-Za-z\d]{8,}$', password):
        flash('Password must be at least 8 characters long and contain both letters and numbers.', 'danger')
        return render_template('register.html')
    if password != confirm_password:
        flash('Passwords do not match.', 'danger')
        return render_template('register.html')
    if not re.match(r'^[a-zA-Z0-9]+$', username):
        flash('Username must only contain letters and numbers.', 'danger')
        return render_template('register.html')
    if is_username_taken(username):
        flash('Username already exists.', 'danger')
        return render_template('register.html')

    # Hash the password and register the user
    hashed_password = hash_password(password)
    add_user(username, hashed_password, email)

    # Fetch the newly registered user from the database
    user = get_user_by_username(username)

    # Set session data (including user_id)
    set_session(user_id=user['id'], username=user['username'], email=user['email'])
    return redirect(url_for('index'))

# Execute Command Route
@app.route('/command', methods=['GET', 'POST'])
@login_required
def command():
    executed_command = None
    command_result = None
    if request.method == 'POST':
        # Fake command execution
        executed_command = request.form.get('command')
        command_result = f"Result of {executed_command}"  # Simulate a command result

    user_commands = get_commands_by_user_id(session.get('user_id'))
    return render_template('command.html', executed_command=executed_command, command_result=command_result, commands=user_commands)

# Save Command Pop-up Route
@app.route('/save_command_popup')
@login_required
def save_command_popup():
    # Debugging
    command = request.args.get('command')
    print(f"Command passed to popup: {command}")
    return render_template('save_command_popup.html')

# Save Command Handler
@app.route('/save_command', methods=['POST'])
@login_required
def save_command():
    command_name = request.form.get('command_name')
    command_description = request.form.get('command_description')
    command_text = request.form.get('command_text')

    # Debugging: Check if data is received correctly
    print(f"Command Name: {command_name}")
    print(f"Command Description: {command_description}")
    print(f"Command Text: {command_text}")

    if command_name and command_description and command_text:
        user_id = session.get('user_id')
        print(f"User ID: {user_id}")  # Debugging: Check user_id

        # Save the command using separate fields for name, text, and description
        add_command(user_id, command_name, command_text, command_description)
        flash('Command saved successfully!', 'success')
    else:
        print("Missing data - not saving command")
    
    return redirect(url_for('command'))

@app.route('/search_commands')
@login_required
def search_commands():
    query = request.args.get('query', '')
    user_id = session.get('user_id')

    if query:
        # Return filtered commands if there is a query
        commands = search_commands_by_name(user_id, query)
    else:
        # Return all commands if the query is empty
        commands = get_commands_by_user_id(user_id)

    # Prepare the commands in a JSON-friendly format
    result = [{
        'command_name': command[0],  # command_name is at index 0
        'command_text': command[1],  # command_text is at index 1
        'command_description': command[2],  # command_description is at index 2
        'created_at': command[3]  # created_at is at index 3
    } for command in commands]

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
