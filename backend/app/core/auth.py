from typing import Optional
from fastapi.security import OAuth2PasswordBearer
from fastapi import Depends, HTTPException
from http import HTTPStatus
from jwt import DecodeError, decode
from pydantic import EmailStr
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.core.deps import get_db_session
from app.core.security import security
from app.core.settings import settings
from app.core.models import User
from app.schemas.token_schema import TokenData


oauth2_schema = OAuth2PasswordBearer(tokenUrl=f"{settings.api.api_prefix}/auth/token")


async def authenticate_user(
    email: EmailStr, password: str, session: AsyncSession
) -> Optional[User]:

    query = select(User).filter(User.email == email)
    result = await session.execute(query)
    user = result.scalars().first()

    if not user:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Email ou senha incorreto.",
        )

    if not security.verify_password(password, user.password):
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Email ou senha incorreto.",
        )

    if not user.is_active:
        raise HTTPException(
            status_code=HTTPStatus.BAD_REQUEST,
            detail="Sua conta foi desativada.",
        )

    return user


async def get_current_user(
    token: str = Depends(oauth2_schema),
    session: AsyncSession = Depends(get_db_session),
) -> User:

    credentials_exception = HTTPException(
        status_code=HTTPStatus.UNAUTHORIZED,
        detail="Não foi possível validar as credenciais.",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode(
            token, settings.jwt.secret_key, algorithms=[settings.jwt.algorithm]
        )
        username: str = payload.get("sub")

        if not username:
            raise credentials_exception

        token_data = TokenData(username=username)

    except DecodeError:
        raise credentials_exception

    query = select(User).filter(User.username == token_data.username)
    result = await session.execute(query)
    user = result.scalars().first()

    if not user:
        raise credentials_exception

    return user
