from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from fastapi import HTTPException, Request
from.utils import decode_access_token

class AccessTokenBearer(HTTPBearer):

    def __init__(self, auto_error: bool = True):
        super().__init__(auto_error=auto_error)

    async def __call__(self, request: Request) -> HTTPAuthorizationCredentials | None:
        creds = await super().__call__(request)

        token = creds.credentials

        token_data = decode_access_token(token)

        if not self.verify_token(token):
            raise HTTPException(status_code=401, detail="Invalid or expired token")

        if token_data["refresh"]:
            raise HTTPException(status_code=401, detail="Provide an access token")

        return creds

    def verify_token(self, token: str) -> bool:

        token_data = decode_access_token(token)

        if token_data is None:
            return False
        return True