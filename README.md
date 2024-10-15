– – – – – – Readme starting point – – – – – –
# Simple Banking System Frontend

## Features Worked On:
- User registration
- User authentication (login/logout)
- User account dashboard
- Transaction management
- Responsive design for various devices

---

## Features:
- **User Registration**: Users can register by providing their first name, last name, phone number, email, local address, and password.
- **User Authentication**: Implements a unique SHA-256 generated address for login along with password verification using bcrypt.
- **Admin Dashboard**: Admins can manage user accounts (create, activate, delete, hold) and monitor transactions.
- **Transaction System**: Allows peer-to-peer transactions, with balance checks and transaction history.
- **Form Validation**: Client-side validation for login and registration forms to ensure data integrity.
- **Responsive Design**: The application is designed to work on various screen sizes, providing a seamless user experience.
## New features
Transaction Interface:
Implemented a new user-friendly interface for handling transactions. Users can now send peer-to-peer transactions, view their transaction history, and manage their accounts (ADD/DELETE/UPDATE operations).
Dashboard:
The user dashboard now displays essential details like user profile information, transaction history, and available account balance. It provides a clear overview of all accounts associated with the user and is designed for easy navigation.
Profile Page:
A dedicated profile interface has been created where users can view and update their personal details. This page is responsive and integrates seamlessly with the dashboard.
Login & Registration Pages:
Completed the styling and form validation logic for both login and registration pages. These interfaces ensure secure user authentication and account creation.


## State:
- The front-end is structured using HTML5 for markup and CSS3 for styling.
- JavaScript is used for interactivity and fetching data through the Fetch API.
- The application is organized into directories for better maintainability:
  - **public/**: Contains static files served to the client (HTML, favicon, manifest).
  - **src/**: Holds all source files including assets, components, contexts, pages, styles, and JavaScript functionality.
  - **package.json**: Manages project dependencies and scripts.

– – – – – – Readme Endpoint – – – – – –