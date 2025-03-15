import os
from flask import Flask
from flask_cors import CORS

from dotenv import load_dotenv

from src.util.database import db_init
# init db
db_init()

from src.util.extensions import socketio
from src.routes.user_routes import *
from src.routes.site_routes import *

# import project source folder
import sys
sys.path.append("src")

# load .env file
load_dotenv()

#
#	App Config
#
app = Flask(__name__)
CORS(app)
app.secret_key = os.getenv('SECRET_KEY')

socketio.init_app(app)

#
#	Blueprints
#
app.register_blueprint(user_bp)
app.register_blueprint(site_bp)

if __name__ == '__main__':
	socketio.run(app, host='0.0.0.0', port=5000, use_reloader=False, debug=True, allow_unsafe_werkzeug=True)