from http import HTTPStatus
from urllib.parse import urlencode

from flask import Blueprint, request, jsonify
from flask import redirect, url_for, session, current_app

from ..services.user_service import *
from ..util.encrypt import *

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/')
def hello_world():
    email = dict(session).get('email', None)
    return f'Hello, you are logged in as {email}!' if email else 'Hello, you are not logged in!'


@auth_bp.route('/login', methods=['GET', 'POST'])
def login() -> jsonify:
    if request.method == 'POST':
        # Fetch user credentials
        email = request.json.get('email')
        password = request.json.get('password')

        # Encrypt password for credentials verification
        encrypted_password = encrypt(password)

        # Credentials validation
        if email and password:
            session['email'] = email

            # Retrieve teacher based on email
            response = get_user_by_email_and_password(email, encrypted_password)

            if "error" in response:
                return jsonify({"status": "error",
                                "message": response["error"]}), HTTPStatus.BAD_REQUEST

            return jsonify({
                'user_data': response,
            }), HTTPStatus.OK

        else:
            return jsonify({'message': 'Invalid credentials'}), HTTPStatus.BAD_REQUEST

    else:
        print('Google OAuth 2.0')
        # Handle case when the user logs in via OAuth2.0
        google = current_app.config['oauth_manager'].get_provider('google')
        redirect_uri = url_for('auth.authorize', _external=True)
        return google.authorize_redirect(redirect_uri)


@auth_bp.route('/authorize')
def authorize() -> jsonify:
    print('Redirected')
    google = current_app.config['oauth_manager'].get_provider('google')
    token = google.authorize_access_token()
    print(token)

    # Retrieve the access token
    access_token = token['access_token']
    resp = google.get('userinfo')

    # Retrieve user data
    user_info = resp.json()
    user_email = user_info['email']

    # Check if email already exists
    response = available_email(user_email)
    print(response)

    if response:
        print('Email doesn\'t exist')
        # Generate random password
        user_password = generate_random_password()

        # Encrypt the generated password
        user_password_encrypted = encrypt(user_password)

        # Insert the new user into db
        user_data = User(user_email, user_password_encrypted)
        user = create_user(user_data)

        # Store email in session
        session['email'] = user_email

        # Make the session permanent
        session.permanent = True

    else:
        print('Email already exists.')
        user = get_user_by_email(user_email)
        print(user)

    # Serialize user data
    query_params = urlencode({
        "access_token": access_token,
        "user_data": user,
    })

    callback_url = f"http://localhost:4200/auth/callback?{query_params}"
    return redirect(callback_url)


@auth_bp.route('/logout')
def logout() -> redirect:
    for key in list(session.keys()):
        session.pop(key)
    return redirect('/')
