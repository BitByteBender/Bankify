Bankify
Fortified by Security, Strengthened by Trust

Overview Bankify is a capstone project developed as part of our final task at ALX/Holberton School for Cohort 1 Hybrid Software Engineers. 

This project is a culmination of all the knowledge and skills we've gained throughout the program. It incorporates key principles of web development, API architecture, security, and database management, all applied to a robust banking/transactional system. 

Our goal was to build a simple yet secure and efficient banking platform that handles user transactions, manages accounts, and ensures data consistency—all while providing a seamless user experience.



Team Members:

Soufiane Sadgali || Project Manager & Backend Architect

Mohammed Shab || Solution Tester

Olatunji Oluwadare || Backend Engineer || tunjidare2@yahoo.com || Github - DevTunechi 

Justus Ndegwa || Frontend Engineer



Technology & Architecture
Backend (Server-Side):

Language: Python
Web Framework: FlaskDatabase: MySQL
ORM: SQLAlchemy
Database Connector: MySQLdb
API Framework: RESTful API
Session Management: Flask Sessions

Frontend (Client-Side):
Markup Language: HTML5
Styling: CSS3
Interactivity: DOM (Document Object Model)
Data Fetching: Fetch API (for making API requests)

Architecture:MVC (Model, View, Controller):
Models: Define the data structures for entities like Users, Accounts, and Transactions, and manage database storage via SQLAlchemy.

Views: Handle user requests, fetch data from the backend via API, and render HTML templates.

Controllers: Contain the logic that processes incoming requests, interacts with models, and returns the correct response.

API-Driven:
The frontend communicates with the backend entirely through RESTful API calls, making the application modular and scalable.

Project Inspiration: The Story Behind BankifyWe chose to create a banking/transaction system because it integrates all the key skills we've learned, from web development to data security. Banking is more than just managing money—it's about building trust, securing user data, and ensuring a smooth and efficient user experience.

This project challenged us to design a reliable and scalable system, where users feel confident about their financial security. The problem-solving process allowed us to apply practical coding techniques and taught us valuable lessons in security, data integrity, and system architecture. 

Bankify reflects our passion and dedication to building something meaningful. 


Development Process, Collaboration, and TimelineProcess:
We adopted an agile methodology for this project. Key phases included:

Planning:
Defining the project's core requirements and goals, selecting the technology stack, and assigning roles within the team.

Frontend Development:
Led by Justus, the frontend involved creating HTML templates, styling with CSS, and ensuring smooth integration with backend API calls.

Backend Development:
Soufiane and Olatunji focused on setting up API routes, database models, and managing connections between the frontend and backend using Flask.

Testing:
Mohammed took responsibility for rigorous testing, ensuring that all features work as expected and identifying any bugs early on.Collaboration:

Daily standups to review progress, discuss blockers, and set priorities. Constant testing and refining of features. Feedback loops to refine UI/UX based on usability tests.

Timeline:Database Structure Setup: Define and implement the schema for users, accounts, and transactions.

API Implementation: Build and document the API routes to enable communication between frontend and backend.

Dashboard: Create a user interface for account management and viewing transaction history.

Authentication: Implement secure user authentication, including login/logout and session management.

Core Banking Features: Implement deposit, withdrawal, and balance check functionalities.

Check out our Trello Board for more detailsChallenges Encountered

Transaction Handling: Ensuring accurate balance calculations and managing concurrent transactions was a significant challenge.

Multi-User Management: Avoiding data conflicts while multiple users accessed the system simultaneously required careful planning.

Error Handling: Handling issues like insufficient funds or network errors in a user-friendly way was another hurdle. 

Data Persistence: Ensuring that transaction data remained consistent across sessions and properly stored in the database was critical.


Learning Objectives

Core Banking Functionalities: We gained a deeper understanding of how to accurately implement key functionalities like deposits, withdrawals, and balance checks.

Concurrency Handling: We explored techniques for managing concurrency in a transactional system, ensuring data integrity.

System Integrity: We learned how to maintain a secure and stable system that safeguards users' financial data and maintains trust.


Conclusion

Bankify represents not only the skills we've learned but also the collaborative spirit that drove us to complete this project. We are proud of the result and believe it reflects our understanding of full-stack development, secure coding practices, and efficient project management.

We hope this system demonstrates our readiness to take on real-world challenges in software engineering.
