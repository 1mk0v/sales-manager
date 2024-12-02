import jwt
import logging
from datetime import timedelta, datetime
from .models import Token

logger = logging.getLogger('uvicorn.error')

class TokenCreater:

    def __init__(
            self,
            secret_key:str,
            algorithm:str,
            validity:int
    ) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.validity = int(validity)

    def getJWT(self, username:str, scopes:list = ['']) -> Token:
        access_token_expires = timedelta(
            days=int(self.validity/(24*60)),
            hours=int(self.validity/(60)),
            minutes=int(self.validity%60)
        )
        access_token = self.create_access_token(
            data={"sub": username, "scopes": " ".join(scopes)},
            expires_delta=access_token_expires
        )
        logger.debug('Create token')
        return Token(access_token=access_token, token_type='Bearer')

    def create_access_token(self, data: dict, expires_delta: timedelta | None = timedelta(minutes=30)):
        to_encode = data.copy()
        expire = datetime.utcnow() + expires_delta
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
        return encoded_jwt