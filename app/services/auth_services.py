from passlib.context import CryptContext


class Auth:
    pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

    async def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)

    async def get_password_hash(self, password: str):
        return self.pwd_context.hash(password)


auth_service = Auth()
