Got it! Here’s a cleaner and more organized version of the README.md with separate sections for commands, explanations, and spaces prepared for images. The explanations are accompanied by placeholders for images that you can fill in later.

# Data Extraction Tool

This repository contains a Flask web application developed as part of an internship project at Micron Memory Malaysia. It is designed to streamline data extraction processes, providing engineers with a user-friendly interface for command execution and management.

## Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Setup](#setup)
- [Usage](#usage)
- [Detailed Procedure](#detailed-procedure)
- [Screenshots](#screenshots)
- [Future Improvements](#future-improvements)

## Introduction

The Data Extraction Tool is a web-based application built with Flask, Python, and SQLite3. It provides functionalities like user authentication, command execution, and command management, aiming to enhance the productivity of engineers during data analysis.

## Features

- User authentication with secure login and registration.
- Execute and manage custom commands.
- Save, modify, and delete commands for reuse.
- Intuitive interface with support for both default and custom input formats.
- SQLite3 database for storing user data and command history.

## Setup

### Prerequisites

- Python 3.7 or higher

### Installation

Clone the repository and set up the environment:

```bash
git clone ssh://git@bitbucket.micron.com/nvburn/data_extraction_tool.git
cd data_extraction_tool
export SECRET_KEY='your_secret_key_here'  # Replace with a randomly generated secret key

Install the required Python packages:

pip install Flask==2.2.2 Flask-Session==0.8.0 argon2-cffi==21.3.0

Usage

To run the application locally, use the following command:

/home/flasheng/anaconda_py37/bin/flask run -h siltse06 -p 3000

Access the application at http://siltse06:3000.

Detailed Procedure

1. User Registration/Log-in

	•	Login Page: Users with an existing account can enter their credentials to log in. If the details are correct, users are redirected to the home page.

	•	Registration Page: New users can create an account by filling in the registration form with a username, email, and password. Upon successful registration, users are redirected to the home page.

2. Home Page Interaction

	•	Home Page: After logging in, users are greeted with a personalized message. The home page provides an overview of the application, descriptions of available tools, and a feedback link for user comments.

3. Using Data Extraction Tools

	•	Tool Selection: Users can select a data extraction tool from the top tabs (e.g., TSUMS, FRPT).
	•	Input Commands:
	•	Default Input: Enter commands in the predefined format, e.g.,

tsums -dbase=b47r -format=revision,version,equation,sites_per_slot


	•	Freeform Input: Paste a custom command directly into the input field for execution.

4. Saving and Managing Commands

	•	Save Command: Users can save executed commands for future use. A pop-up will appear, prompting for a name and description.

	•	Manage Saved Commands: Users can view, modify, or delete saved commands through the “Saved Commands” tab. A search bar allows filtering by name or description.

	•	Modify Saved Commands: Users can modify existing saved commands through a pop-up interface.

5. Viewing Command Execution Results

	•	Terminal Output: The output of executed commands is displayed in a terminal-style section at the bottom of each tool page. Users can copy the output with a single click.

Screenshots

Include screenshots of the application’s key features for better understanding:

	•	

	•	

	•	

	•	

	•	

	•	

	•	

	•	

Future Improvements

	•	WSGI Server: Integrate a WSGI server like Gunicorn to improve performance and manage concurrent requests.
	•	Command Execution Tracking: Add a feature to track command execution, similar to Linux’s top command, showing real-time usage stats.
	•	Database Upgrade: Consider switching to MySQL or PostgreSQL for improved speed and handling of larger datasets.

Conclusion

The Data Extraction Tool streamlines data analysis for engineers at Micron, offering a user-friendly way to execute commands and manage data retrieval. Its intuitive interface and robust backend make it a valuable asset for engineering teams.

### Key Updates:
- **Commands in Code Blocks**: All bash commands are in separate code blocks.
- **Text Separations**: Explanations are in plain text for better readability.
- **Image Placeholders**: Specific spaces are prepared for images that correspond to each explanation. You can replace `path_to_*_image.png` with the actual paths to your screenshots.
- **Detailed Procedure**: Each step of the application is described in a dedicated section with the corresponding space for images.

This format is designed to be clear and easy to follow for users and developers alike.