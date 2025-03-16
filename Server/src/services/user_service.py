from ..model.user import User
from ..dto.user_dto import UserDTO
from ..util.database import db
from ..util.encrypt import encrypt
from google.cloud.firestore_v1.base_query import FieldFilter

#
#	Path for users
#
USERS_COLLECTION = "users"

#
#	DB Fetch
#
def get_user_by_email(email: str) -> dict:
	try:
		# DB Fetch
		users_ref = db.collection(USERS_COLLECTION)
		query = users_ref.where(filter=FieldFilter('email', '==', email))
		docs = query.get()

		if not docs:
			return {"error": "No user found with the provided email"}

		# Assuming email is unique, return the first document
		user = docs[0].to_dict()
		return user

	except Exception as e:
		# Log the error for debugging
		return {"error": str(e)}

def get_user_by_email_and_password(email: str, password: str) -> dict:
	try:
		users = list(db.collection(USERS_COLLECTION)
			   	.where(filter=FieldFilter('email', '==', email))
				.where(filter=FieldFilter('password', '==', password))
				.stream())
		if len(users) == 0:
			return {}
		user_doc = users[0]
		user_data = user_doc.to_dict()

		user_dto = UserDTO(user_doc.id,user_data['email'],user_data['password'])

		return user_dto.to_dict()
	except Exception as e:
		return {"error" : str(e)}

def available_email(email: str) -> bool:
	print(email)
	# Fetch data from db
	users_ref = list(db.collection(USERS_COLLECTION).where(filter=FieldFilter('email', '==', email)).stream())

	# Check existence
	if len(users_ref) > 0:
		return False

	return True


#
#	CRUD operations
#
def create_user(data: User) -> dict:
	try:
		data.password = encrypt(data.password)
		_,user_ref = db.collection(USERS_COLLECTION).add(data.to_dict())
		return UserDTO(user_ref.id, data.email, data.password).to_dict()

	except Exception as e:
		return {"error": str(e)}
