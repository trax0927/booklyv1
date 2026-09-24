from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import Depends, HTTPException, Request
from.utils import decode_access_token
from src.db.redis import is_token_blacklisted
from sqlmodel.ext.asyncio.session import AsyncSession
from src.db.main import get_session
from .service import UserService
from typing import List

userService = UserService()

class TokenBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        token = creds.credentials

        token_data = decode_access_token(token)

        if not self.verify_token(token):
            raise HTTPException(status_code=403, detail="Invalid or expired token, please get a new token")

        if await is_token_blacklisted(token_data['jti']):
            raise HTTPException(status_code=403, detail="Token has been revoked, please get a new token")


        self.verify_token_data(token_data)


        return token_data

    def verify_token(self, token: str) -> bool:

        token_data = decode_access_token(token)

        if token_data is None:
            return False
        return True

    def verify_token_data(self, token_data):
        raise NotImplementedError("Subclasses must implement the verify_token_data method.")

# check if the token is an access token or a refresh token
class AccessTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and token_data['refresh']:
            raise HTTPException(status_code=403, detail="Provide an access token")

class RefreshTokenBearer(TokenBearer):
    def verify_token_data(self, token_data: dict) -> None:
        if token_data and not token_data['refresh']:
            raise HTTPException(status_code=403, detail="Provide a refresh token")

async def get_current_user(
        token_details: dict = Depends(AccessTokenBearer()),
        session: AsyncSession = Depends(get_session)
        ):

    user_email = token_details['user']['email']

    user = await userService.get_user_by_email(user_email, session)

    return user

class RoleChecker:
    def __init__(self, required_roles: List[str]) -> None:
        self.required_roles = required_roles

    async def __call__(self, current_user = Depends(get_current_user)):
        if current_user.role in self.required_roles:
            return True

        raise HTTPException(status_code=403, detail="You do not have permission to access this resource")