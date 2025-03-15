import os
import firebase_admin
from firebase_admin import credentials, firestore
from dotenv import load_dotenv

# load
load_dotenv()

#
#	Database config
#
cred = credentials.Certificate(os.getenv('FIREBASE_PATH'))

# init
firebase_admin.initialize_app(cred)

db = firestore.client()