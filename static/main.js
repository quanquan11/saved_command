// This script can be used for global JS logic that applies across all pages

// Example of toggling tab visibility
function toggleTab(tabName) {
    const tabs = document.getElementsByClassName('tablinks');
    for (let i = 0; i < tabs.length; i++) {
        tabs[i].classList.remove('active');
    }

    const tabContent = document.getElementsByClassName('tabcontent');
    for (let i = 0; i < tabContent.length; i++) {
        tabContent[i].style.display = 'none';
    }

    document.getElementById(tabName).style.display = 'block';
    event.currentTarget.classList.add('active');
}
