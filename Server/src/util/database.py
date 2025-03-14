import os
import firebase_admin
from firebase_admin import credentials, db
from dotenv import load_dotenv

# load
load_dotenv()

#
#	Database config
#
def db_init():
	# fetch
	cred = credentials.Certificate(os.getenv('FIREBASE_PATH'))

	# init
	firebase_admin.initialize_app(cred, {
		'databaseURL': 'https://itfest-2025-fake-news-default-rtdb.europe-west1.firebasedatabase.app/'
	})