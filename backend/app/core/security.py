from pwdlib import PasswordHash
from jwt import encode
from zoneinfo import ZoneInfo
from datetime import datetime, timedelta
from app.core.settings import settings


class Security:
    def __init__(self):
        self.pwd_context = PasswordHash.recommended()

    def get_password_hash(self, password) -> str:
        return self.pwd_context.hash(password)

    def verify_password(self, plain_password, hashed_password) -> bool:
        return self.pwd_context.verify(plain_password, hashed_password)

    def create_access_token(self, data: dict) -> str:

        to_encode = data.copy()
        expire = datetime.now(tz=ZoneInfo(settings.timezone.timezone)) + timedelta(
            minutes=settings.jwt.expire_minutes
        )

        to_encode.update({"exp": expire})
        encoded_jwt = encode(
            to_encode, settings.jwt.secret_key, algorithm=settings.jwt.algorithm
        )

        return encoded_jwt


security = Security()
