// auth.js

let isAuthenticated = false;

export function login(username, password) {
    // Simulated API call for authentication
    return new Promise((resolve, reject) => {
        // Replace with your actual API endpoint and logic
        const apiUrl = 'https://api.yourbankingapp.com/login';
        
        fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ username, password }),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Login failed');
            }
            return response.json();
        })
        .then(data => {
            isAuthenticated = true;
            localStorage.setItem('token', data.token); // Store token for session
            resolve(data);
        })
        .catch(error => {
            reject(error);
        });
    });
}

export function logout() {
    isAuthenticated = false;
    localStorage.removeItem('token'); // Clear token on logout
}

// Function to check authentication status
export function isUserAuthenticated() {
    return isAuthenticated;
}