from datetime import datetime, timedelta
from flask_mail import Mail, Message
from werkzeug.security import generate_password_hash, check_password_hash
from app.models import OTP, db

mail = Mail()


def create_user(data):
    # Logic to insert a new user into the database
    pass

def update_user(user_id, data):
    # Logic to update a user's information
    pass

def find_user_by_id(user_id):
    # Logic to retrieve a single user by their ID
    pass

def find_all_users():
    # Logic to retrieve all users
    pass

def delete_user(user_id):
    # Logic to delete a user from the database
    pass

def hold_user_account(user_id):
    # Logic to freeze/hold a user account
    pass

def generate_otp():
    """Generate a secure 6-digit OTP code."""
    import secrets
    otp = secrets.randbelow(1000000)
    return f'{otp:06}'

def send_otp_email(user_email, otp_code):
    """Send the OTP code to the user's email."""
    msg = Message(subject="Your Bankify OTP Code",
                  sender='noreply@bankify.io',
                  recipients=[user_email])
    msg.body = f"Your OTP code is {otp_code}. It will expire in 5 minutes."
    mail.send(msg)

def create_otp(user_id):
    """Generate and store an OTP for the user."""
    otp_code = generate_otp()
    hashed_otp = generate_password_hash(otp_code)

    expiration_time = datetime.utcnow() + timedelta(minutes=5)
    otp_entry = OTP(user_id=user_id, otp_code=hashed_otp, expires_at=expiration_time)
    db.session.add(otp_entry)
    db.session.commit()

    return otp_code

def validate_otp(user_id, otp_code):
    """Validate if the provided OTP is correct and not expired."""
    otp_entry = OTP.query.filter_by(user_id=user_id).first()

     if otp_entry and check_password_hash(otp_entry.otp_code, otp_code) and otp_entry.is_valid():
         return True
     return False
