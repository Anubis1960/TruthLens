from http import HTTPStatus
from flask import jsonify, request, Blueprint

from src.services.user_service import *

USER_URL = '/api/users'


user_bp = Blueprint('users', __name__, url_prefix=USER_URL)


@user_bp.route('/register', methods=['POST'])
def add_user() -> jsonify:
    user_data = request.get_json()
    print(user_data)

    try:
        user = User.from_dict(user_data)

        # response
        response = create_user(user)

        if 'error' in response:
            return jsonify(response), HTTPStatus.BAD_REQUEST

        return jsonify(response), HTTPStatus.CREATED

    except Exception as e:
        return jsonify({'error': str(e)}), HTTPStatus.BAD_REQUEST
