from passlib.context import CryptContext


class Security:
    def __init__(self):
        self._pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')

    def verify_password(self, password: str, hash: str) -> bool:
        return self._pwd_context.verify(password, hash)

    def get_password_hash(self, password: str) -> str:
        return self._pwd_context.hash(password)


security = Security()
