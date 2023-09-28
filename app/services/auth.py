from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials

from app.schemas.token_schemas import TokenModel


class AuthService:
    def __init__(self, auth_repo):
        self.auth_repo = auth_repo()

    async def login(self, body: OAuth2PasswordRequestForm) -> TokenModel:
        return await self.auth_repo.login(body)

    async def refresh_token(self, credentials: HTTPAuthorizationCredentials) -> TokenModel:
        return await self.auth_repo.refresh_token(credentials)

