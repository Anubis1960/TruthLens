import sys
from flask import Flask
from flask_cors import CORS
from src.model.oauthmanager import OAuthManager
from src.routes.auth_routes import *
from src.routes.chat_routes import *
from src.routes.site_routes import *
from src.routes.upload_routes import *
from src.routes.user_routes import *
from src.util.extensions import socketio

sys.path.append("src")

# load .env file
load_dotenv()

app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv('SECRET_KEY')

socketio.init_app(app)

# OAuth Manager Setup
oauth_manager = OAuthManager(app)
app.config['oauth_manager'] = oauth_manager

app.register_blueprint(user_bp)
app.register_blueprint(site_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(chat_bp)

if __name__ == '__main__':
    socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=True, allow_unsafe_werkzeug=True)
