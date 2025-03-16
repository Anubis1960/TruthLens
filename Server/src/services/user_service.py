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
#	CRUD operations
#
def create_user(data: User) -> dict:
	try:
		users=list(db.collection(USERS_COLLECTION)
					.where('email', '==', data.email)
					.stream())
		if len(users) > 0:
			return {"error": "Email already in use"}
		data.password = encrypt(data.password)
		_,user_ref = db.collection(USERS_COLLECTION).add(data.to_dict())
		return UserDTO(user_ref.id, data.email, data.password).to_dict()

	except Exception as e:
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
		
		