from ..model.user import User
from ..dto.user_dto import UserDTO
from firebase_admin import db

#
#	Path for users
#
DB_REF = 'fake-news/user'
REF = db.reference(DB_REF)

#
#	CRUD operations
#
def create_user(data: User) -> dict:
	try:
		user_ref = REF.push(data.to_dict())
		user_dto = UserDTO(user_ref.key, data.email, data.password)
		return user_dto.to_dict()

	except KeyError as e:
		return {"error": f"Key missing: {e}"}
