// Fetch saved commands from the server for TSUMS
function executeCommand() {
    const command = document.getElementById('command-input').value;
    if (command) {
        fetch('/frpt', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/x-www-form-urlencoded',
            },
            body: new URLSearchParams({ command })
        })
        .then(response => response.json())
        .then(result => {
            document.getElementById('terminal-output').textContent = result.message;
            document.getElementById('executed-command-container').style.display = 'block';
        })
        .catch(error => {
            console.error('Error executing command:', error);
            document.getElementById('terminal-output').textContent = 'Error executing command.';
        });
    } else {
        alert('Please enter a command before executing.');
    }
}

function openSavePopup() {
    const command = document.getElementById('command-input').value;
    const category_id = 2;  // Assuming 2 is for FRPT
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

function showAllCommands() {
    const savedCommandsBody = document.getElementById('saved-commands-body');
    savedCommandsBody.innerHTML = ''; // Clear previous results

    fetch(`/get_saved_commands?category_id=2`)  // FRPT category_id = 2
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

    fetch(`/get_saved_commands?category_id=2`)  // category_id=2 is for FRPT
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
