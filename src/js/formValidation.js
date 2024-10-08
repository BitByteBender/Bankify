// formValidation.js

// Function to validate login form
function validateLoginForm() {
    const email = document.querySelector('#loginEmail').value;
    const password = document.querySelector('#loginPassword').value;

    if (!email || !password) {
        alert('Both email and password are required.');
        return false;
    }

    // Additional validation checks can be added here
    return true;
}

// Function to validate registration form
function validateRegistrationForm() {
    const email = document.querySelector('#registerEmail').value;
    const password = document.querySelector('#registerPassword').value;
    const confirmPassword = document.querySelector('#confirmPassword').value;

    if (!email || !password || !confirmPassword) {
        alert('All fields are required.');
        return false;
    }

    if (password !== confirmPassword) {
        alert('Passwords do not match.');
        return false;
    }

    return true;
}

// Event listeners for form submissions
document.addEventListener('DOMContentLoaded', () => {
    const loginForm = document.querySelector('#loginForm');
    if (loginForm) {
        loginForm.addEventListener('submit', (event) => {
            if (!validateLoginForm()) {
                event.preventDefault();
            }
        });
    }

    const registrationForm = document.querySelector('#registrationForm');
    if (registrationForm) {
        registrationForm.addEventListener('submit', (event) => {
            if (!validateRegistrationForm()) {
                event.preventDefault();
            }
        });
    }
});