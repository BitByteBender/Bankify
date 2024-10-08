// transactions.js

export function getTransactionHistory() {
    const token = localStorage.getItem('token'); // Get token from local storage

    return new Promise((resolve, reject) => {
        // Replace with your actual API endpoint and logic
        const apiUrl = 'https://api.yourbankingapp.com/transactions/history';
        
        fetch(apiUrl, {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch transaction history');
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

export function createTransaction(transactionData) {
    const token = localStorage.getItem('token'); // Get token from local storage

    return new Promise((resolve, reject) => {
        // Replace with your actual API endpoint and logic
        const apiUrl = 'https://api.yourbankingapp.com/transactions';

        fetch(apiUrl, {
            method: 'POST',
            headers: {
                'Authorization': `Bearer ${token}`,
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(transactionData),
        })
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to create transaction');
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