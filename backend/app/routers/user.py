from fastapi import APIRouter, Depends
from fastapi.security import OAuth2PasswordRequestForm
from http import HTTPStatus

from sqlalchemy.ext.asyncio import AsyncSession

from uuid import UUID

from app.core.auth import get_current_user
from app.core.deps import get_db_session
from app.core.models import User
from app.use_cases.user import UserUseCase

from app.schemas.user_schema import (
    UserSchema,
    UserSchemaUpdate,
    UserSchemaList,
    UserSchemaDevices,
)
from app.schemas.message_schema import MessageSchema
from app.schemas.token_schema import Token

router = APIRouter(tags=["USERS"])


@router.post("/users", response_model=MessageSchema, status_code=HTTPStatus.CREATED)
async def create_user(
    user: UserSchema, session: AsyncSession = Depends(get_db_session)
):

    user_uc = UserUseCase(session)
    result = await user_uc.create_user(user)

    return result


@router.get("/users", response_model=UserSchemaList, status_code=HTTPStatus.OK)
async def list_users(
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 10,
):

    user_uc = UserUseCase(session)
    result = await user_uc.list_users(skip=skip, limit=limit)
    return result


@router.get(
    "/users/{user_id}",
    response_model=UserSchemaDevices,
    status_code=HTTPStatus.OK,
)
async def get_user(
    user_id: UUID,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):

    user_uc = UserUseCase(session)
    result = await user_uc.get_user(user_id)
    return result


@router.put(
    "/users/{user_id}",
    response_model=MessageSchema,
    status_code=HTTPStatus.ACCEPTED,
)
async def update_user(
    user_id: UUID,
    user: UserSchemaUpdate,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):

    user_uc = UserUseCase(session)
    result = await user_uc.update_user(user_id, user)
    return result


@router.delete(
    "/users/{user_id}",
    response_model=MessageSchema,
)
async def delete_user(
    user_id: UUID,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):

    user_uc = UserUseCase(session)
    result = await user_uc.delete_user(user_id)
    return result


@router.post("/auth/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    session: AsyncSession = Depends(get_db_session),
):

    user_uc = UserUseCase(session)
    result = await user_uc.login_user(form_data.username, form_data.password)
    return result
