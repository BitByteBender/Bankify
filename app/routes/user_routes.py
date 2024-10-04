from flask import Blueprint, request, jsonify
from app.services.user_service import create_otp, validate_otp, send_otp_email

user_bp = Blueprint('user', __name__)

@user_bp.route('/login', methods=['POST'])
def login():
    user_id = request.json.get('user_id')
    user_email = request.json.get('email')
    
    # Generate OTP and send it to the user's email
    otp_code = create_otp(user_id)
    send_otp_email(user_email, otp_code)
    
    return jsonify({"message": "OTP has been sent to your email"}), 200

@user_bp.route('/verify_otp', methods=['POST'])
def verify_otp():
    user_id = request.json.get('user_id')
    otp_code = request.json.get('otp_code')
    
    # Validate the OTP
    if validate_otp(user_id, otp_code):
        return jsonify({"message": "OTP is valid, user authenticated"}), 200
    else:
        return jsonify({"message": "Invalid or expired OTP"}), 400