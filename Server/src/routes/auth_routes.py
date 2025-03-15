from http import HTTPStatus

from flask import Blueprint, request, jsonify
from ..util.encrypt import encrypt
from ..services.user_service import get_user_by_email_and_password

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/login', methods=['GET', 'POST'])
def login() -> jsonify:
    if request.method == 'POST':
        email = request.json.get('email')
        password = request.json.get('password')

        # Encrypt the password to check credentials
        encrypted_password = encrypt(password)

        print("recived email",email)
        print("received password", password)
        
        if email and password:
            user_data = get_user_by_email_and_password(email,encrypted_password)

            if not user_data:
                return jsonify({'message': 'Invalid credentials'}), HTTPStatus.BAD_REQUEST
        
            return jsonify({
                'user_data': user_data,
            }), HTTPStatus.OK
        else:
            return jsonify({'message': 'Invalid credentials'}), HTTPStatus.BAD_REQUEST
