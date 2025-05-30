class User:
    def __init__(self, email: str, password: str):
        self.email = email
        self.password = password

    def to_dict(self):
        return {
            'email': self.email,
            'password': self.password
        }

    @staticmethod
    def from_dict(data: dict) -> "User":
        user = User(data['email'], data['password'])
        return user
