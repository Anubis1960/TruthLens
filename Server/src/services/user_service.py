from ..model.user import User
from ..dto.user_dto import UserDTO
from ..util.database import db
from ..util.encrypt import encrypt

#
#	Path for users
#
USERS_COLLECTION = "users"

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
