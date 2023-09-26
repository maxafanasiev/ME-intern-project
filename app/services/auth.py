from fastapi.security import OAuth2PasswordRequestForm, HTTPAuthorizationCredentials

from app.schemas.token_schemas import TokenModel


class AuthService:
    def __init__(self, auth_repo):
        self.auth_repo = auth_repo()

    def login(self, body: OAuth2PasswordRequestForm) -> TokenModel:
        tokens = self.auth_repo.login(body)
        return tokens

    def refresh_token(self, credentials: HTTPAuthorizationCredentials) -> TokenModel:
        tokens = self.auth_repo.refresh_token(credentials)
        return tokens

    def get_current_user(self):
        current_user = self.auth_repo.get_current_user()
        return current_user
