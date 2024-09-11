function executeCommand() {
    const command = document.getElementById('command-input').value;
    if (command) {
        // Display executed command result
        document.getElementById('executed-command').textContent = command;
        document.getElementById('executed-command-container').style.display = 'block';
        document.getElementById('terminal-output').textContent = `Executed Command: ${command}`;
        
        // Optionally, send this to the server for processing if needed
        fetch('/tsums', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({ command })
        })
        .then(response => response.json())
        .then(result => {
            // Handle the result from the server if any response is expected
            console.log('Command result:', result);
            document.getElementById('terminal-output').textContent = `Server Response: ${result.message}`;
        })
        .catch(error => {
            console.error('Error executing command:', error);
        });
    } else {
        alert('Please enter a command before executing.');
    }
}

function openSavePopup() {
    const command = document.getElementById('command-input').value;
    const category_id = 1;  // Assuming 1 is for TSUMS
    if (command) {
        const popup = window.open(
            `/save_command_popup?command=${encodeURIComponent(command)}&category_id=${category_id}`,
            'Save Command',
            'width=500,height=400'
        );
        if (!popup) {
            alert('Popup blocked! Please allow popups for this site.');
        }
    } else {
        alert('Please execute a command before saving.');
    }
}


// Fetch saved commands from the server for TSUMS
function showAllCommands() {
    const savedCommandsBody = document.getElementById('saved-commands-body');
    savedCommandsBody.innerHTML = ''; // Clear previous results

    // Make an AJAX request to fetch the saved commands
    fetch(`/get_saved_commands?category_id=1`)  // category_id=1 is for TSUMS
        .then(response => response.json())
        .then(data => {
            if (data.length > 0) {
                data.forEach(command => {
                    const row = `
                        <tr>
                            <td>${command.command_name}</td>
                            <td>${command.command_text}</td>
                            <td>${command.command_description}</td>
                            <td>${command.created_at}</td>
                        </tr>
                    `;
                    savedCommandsBody.insertAdjacentHTML('beforeend', row);
                });
            } else {
                savedCommandsBody.innerHTML = '<tr><td colspan="4">No saved commands found.</td></tr>';
            }
        })
        .catch(error => {
            console.error('Error fetching saved commands:', error);
            savedCommandsBody.innerHTML = '<tr><td colspan="4">Failed to fetch commands. Please try again later.</td></tr>';
        });
}

// Search for commands by name, text, or description
function searchCommands() {
    const query = document.getElementById('search-query').value.toLowerCase();
    const savedCommandsBody = document.getElementById('saved-commands-body');
    savedCommandsBody.innerHTML = ''; // Clear previous results

    fetch(`/get_saved_commands?category_id=1`)  // Fetch TSUMS commands
        .then(response => response.json())
        .then(data => {
            const filteredCommands = data.filter(command => 
                command.command_name.toLowerCase().includes(query) ||
                command.command_text.toLowerCase().includes(query) ||
                command.command_description.toLowerCase().includes(query)
            );

            if (filteredCommands.length > 0) {
                filteredCommands.forEach(command => {
                    const row = `
                        <tr>
                            <td>${command.command_name}</td>
                            <td>${command.command_text}</td>
                            <td>${command.command_description}</td>
                            <td>${command.created_at}</td>
                        </tr>
                    `;
                    savedCommandsBody.insertAdjacentHTML('beforeend', row);
                });
            } else {
                savedCommandsBody.innerHTML = '<tr><td colspan="4">No matching commands found.</td></tr>';
            }
        })
        .catch(error => {
            console.error('Error fetching saved commands:', error);
            savedCommandsBody.innerHTML = '<tr><td colspan="4">Failed to fetch commands. Please try again later.</td></tr>';
        });
}

function openBottomTab(evt, tabName) {
    var i, tabcontent;
    tabcontent = document.getElementsByClassName("bottom-tabcontent");
    
    // Hide all tab contents
    for (i = 0; i < tabcontent.length; i++) {
        tabcontent[i].style.display = "none";
    }

    // Show the specific tab content
    document.getElementById(tabName).style.display = "block";
}

