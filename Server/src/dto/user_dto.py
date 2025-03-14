class UserDTO:
	def __init__(self, id: str, email: str, password: str):
		self.id = id
		self.email = email
		self.password = password

	def to_dict(self):
		return {
			'id': self.id,
			'email': self.email,
			'password': self.password
		}

	@staticmethod
	def from_dict(data: dict) -> "UserDTO":
		user_dto = UserDTO(data['id'], data['email'], data['password'])
		return user_dto