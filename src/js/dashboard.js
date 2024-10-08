// dashboard.js

// Function to load user information
function loadUserInfo() {
    // Fetch user information from the server
    fetch('/api/user-info')
        .then(response => response.json())
        .then(data => {
            // Display user info on the dashboard
            const userInfoDiv = document.querySelector('#userInfo');
            userInfoDiv.innerHTML = `
                <h2>${data.name}</h2>
                <p>Email: ${data.email}</p>
                <p>Balance: $${data.balance}</p>
            `;
        })
        .catch(error => console.error('Error fetching user info:', error));
}

// Initialize dashboard
document.addEventListener('DOMContentLoaded', () => {
    loadUserInfo();
});