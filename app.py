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

app = Flask(__name__)
app.secret_key = os.environ.get('SECRET_KEY', '8667af877d92a14c36b059a0a05c5638')

app.config['SESSION_PERMANENT'] = False
app.config['SESSION_TYPE'] = 'filesystem'
Session(app)

# Initialize the database and close connection after request
init_db(app)

@app.route('/')
@login_required
def index():
    return redirect(url_for('tsums_page'))

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

    hashed_password = hash_password(password)
    add_user(username, hashed_password, email)

    user = get_user_by_username(username)
    set_session(user_id=user['id'], username=user['username'], email=user['email'])
    return redirect(url_for('index'))

@app.route('/tsums', methods=['GET', 'POST'])
@login_required
def tsums_page():
    executed_command = None
    command_result = None
    if request.method == 'POST':
        # Retrieve the command from the POST request
        executed_command = request.form.get('command')
        if executed_command:
            # For now, we will just return the command as a result
            command_result = f"Executed TSUMS command: {executed_command}"

            # Return the result as JSON for the terminal to display
            return jsonify({'message': command_result})
        else:
            return jsonify({'message': 'No command provided'}), 400

    # Fetch user's saved TSUMS commands and render the page
    user_commands = get_commands_by_user_id(session.get('user_id'), category_id=1)
    return render_template('tsums.html', commands=user_commands)


@app.route('/frpt', methods=['GET', 'POST'])
@login_required
def frpt_page():
    executed_command = None
    command_result = None
    if request.method == 'POST':
        executed_command = request.form.get('command')
        command_result = f"Result of FRPT command: {executed_command}"

    user_commands = get_commands_by_user_id(session.get('user_id'), category_id=2)
    return render_template('frpt.html', executed_command=executed_command, command_result=command_result, commands=user_commands)

@app.route('/fdat95', methods=['GET', 'POST'])
@login_required
def fdat95_page():
    executed_command = None
    command_result = None
    if request.method == 'POST':
        executed_command = request.form.get('command')
        command_result = f"Result of FDAT95 command: {executed_command}"

    user_commands = get_commands_by_user_id(session.get('user_id'), category_id=3)
    return render_template('fdat95.html', executed_command=executed_command, command_result=command_result, commands=user_commands)

@app.route('/save_command_popup')
@login_required
def save_command_popup():
    command = request.args.get('command')
    category_id = request.args.get('category_id')
    return render_template('save_command_popup.html', command=command, category_id=category_id)

@app.route('/save_command', methods=['POST'])
@login_required
def save_command():
    command_name = request.form.get('command_name')
    command_description = request.form.get('command_description')
    command_text = request.form.get('command_text')
    category_id = request.form.get('category_id')

    if command_name and command_description and command_text:
        user_id = session.get('user_id')
        add_command(user_id, command_name, command_text, command_description, category_id)
        flash('Command saved successfully!', 'success')
    else:
        flash('Failed to save command.', 'danger')

    return redirect(url_for('tsums_page'))

@app.route('/get_saved_commands', methods=['GET'])
@login_required
def get_saved_commands():
    """
    Fetch saved commands for the logged-in user based on the category.
    The category_id will be passed as a query parameter.
    """
    category_id = request.args.get('category_id')
    user_id = session.get('user_id')

    # Fetch commands by user and category from the database
    commands = get_commands_by_user_id(user_id, category_id)

    result = [{
        'command_name': command['command_name'],
        'command_text': command['command_text'],
        'command_description': command['command_description'],
        'created_at': command['created_at']
    } for command in commands]

    return jsonify(result)

@app.route('/search_commands', methods=['GET'])
@login_required
def search_commands():
    query = request.args.get('query', '')
    category_id = request.args.get('category_id')
    user_id = session.get('user_id')

    if query:
        commands = search_commands_by_name(user_id, query, category_id)
    else:
        commands = get_commands_by_user_id(user_id, category_id)

    result = [{
        'command_name': command[0],
        'command_text': command[1],
        'command_description': command[2],
        'created_at': command[3]
    } for command in commands]

    return jsonify(result)

if __name__ == '__main__':
    app.run(debug=True)
