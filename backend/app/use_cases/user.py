from app.schemas.message_schema import MessageSchema
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, Response
from http import HTTPStatus
from app.core.security import security
from app.core.models import User
from app.core.auth import authenticate_user
from app.schemas.user_schema import (
    UserSchema,
    UserSchemaPublic,
    UserSchemaUpdate,
    UserSchemaList,
    UserSchemaDevices,
)
from app.schemas.token_schema import Token
from uuid import UUID


class UserUseCase:

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_user(self, user: UserSchema) -> UserSchemaPublic:
        new_user = User(
            username=user.username,
            email=user.email,
            password=security.get_password_hash(user.password),
        )

        query = select(User).filter(
            (User.username == new_user.username) | (User.email == new_user.email)
        )
        result = await self._session.execute(query)
        existing_user = result.scalars().first()

        if existing_user:
            if existing_user.username == new_user.username:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail="Por favor, escolha um nome de usuário diferente",
                )
            if existing_user.email == new_user.email:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail="Por favor, escolha um email diferente",
                )

        self._session.add(new_user)
        await self._session.commit()
        return MessageSchema(message="Usuário criado com sucesso")

    async def get_user(self, user_id: UUID) -> UserSchemaDevices:
        query = select(User).filter(User.id == user_id)
        result = await self._session.execute(query)
        user = result.scalars().first()

        if not user:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Usuário não encontrado",
            )

        return user

    async def list_users(self, skip: int = 0, limit: int = 10) -> UserSchemaList:
        query = select(User).offset(skip).limit(limit)
        result = await self._session.execute(query)
        users_db = result.scalars().unique().all()

        if not users_db:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Nenhum usuário encontrado",
            )

        return {"users": users_db}

    async def update_user(
        self, user_id: UUID, user: UserSchemaUpdate
    ) -> UserSchemaPublic:
        query = select(User).filter(User.id == user_id)
        result = await self._session.execute(query)
        user_db = result.scalars().first()

        if not user_db:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Usuário não encontrado",
            )

        if user.username:
            user_db.username = user.username
        if user.email:
            user_db.email = user.email
        if user.password:
            user_db.password = security.get_password_hash(user.password)
        if user.is_active:
            user_db.is_active = user.is_active

        await self._session.commit()
        await self._session.refresh(user_db)
        return MessageSchema(message="Usuário atualizado com sucesso")

    async def delete_user(self, user_id: UUID) -> Response:
        query = select(User).filter(User.id == user_id)
        result = await self._session.execute(query)
        user_db = result.scalars().first()

        if not user_db:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Usuário não encontrado",
            )

        await self._session.delete(user_db)
        await self._session.commit()
        return Response(status_code=HTTPStatus.NO_CONTENT)

    async def login_user(self, username: str, password: str) -> Token:

        user = await authenticate_user(
            email=username, password=password, session=self._session
        )

        if not user:
            raise HTTPException(
                status_code=HTTPStatus.UNAUTHORIZED,
                detail="Credenciais inválidas",
            )

        return Token(
            access_token=security.create_access_token(data={"sub": str(user.username)}),
            type_token="Bearer",
        )
