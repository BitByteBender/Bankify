// user.js

export function getUserProfile() {
    const token = localStorage.getItem('token'); // Get token from local storage

    return new Promise((resolve, reject) => {
        // Replace with your actual API endpoint and logic
        const apiUrl = 'https://api.yourbankingapp.com/user/profile';
        
        fetch(apiUrl, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch user profile');
            }
            return response.json();
        })
        .then(data => {
            resolve(data);
        })
        .catch(error => {
            reject(error);
        });
    });
}

export function updateUserProfile(userData) {
    const token = localStorage.getItem('token'); // Get token from local storage

    return new Promise((resolve, reject) => {
        // Replace with your actual API endpoint and logic
        const apiUrl = 'https://api.yourbankingapp.com/user/profile';

        fetch(apiUrl, {
            method: 'PUT',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(userData),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to update user profile');
            }
            return response.json();
        })
        .then(data => {
            resolve(data);
        })
        .catch(error => {
            reject(error);
        });
    });
}