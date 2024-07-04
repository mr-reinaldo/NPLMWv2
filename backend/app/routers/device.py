from fastapi import APIRouter, Depends
from http import HTTPStatus

from sqlalchemy.ext.asyncio import AsyncSession

from uuid import UUID

from app.core.auth import get_current_user
from app.core.deps import get_db_session
from app.core.models import User
from app.use_cases.device import DeviceUseCase

from app.schemas.device_schema import (
    DeviceSchema,
    DeviceSchemaPublic,
    DeviceSchemaUpdate,
    DeviceSchemaList,
)

from app.schemas.message_schema import MessageSchema


router = APIRouter(tags=["DEVICES"])


@router.post(
    "/devices",
    response_model=MessageSchema,
    status_code=HTTPStatus.CREATED,
)
async def create_device(
    device: DeviceSchema,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):

    device_uc = DeviceUseCase(session)
    result = await device_uc.create_device(device, current_user)

    return result


@router.get(
    "/devices",
    response_model=DeviceSchemaList,
    status_code=HTTPStatus.OK,
)
async def list_devices(
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 10,
):

    device_uc = DeviceUseCase(session)
    result = await device_uc.list_devices(current_user, skip, limit)

    return result


@router.get(
    "/devices/{device_id}",
    response_model=DeviceSchemaPublic,
    status_code=HTTPStatus.OK,
)
async def get_device(
    device_id: UUID,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):

    device_uc = DeviceUseCase(session)
    result = await device_uc.get_device(device_id, current_user)

    return result


@router.put(
    "/devices/{device_id}",
    response_model=MessageSchema,
    status_code=HTTPStatus.ACCEPTED,
)
async def update_device(
    device_id: UUID,
    device: DeviceSchemaUpdate,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):

    device_uc = DeviceUseCase(session)
    result = await device_uc.update_device(device_id, device, current_user)

    return result


@router.delete(
    "/devices/{device_id}",
    response_model=MessageSchema,
)
async def delete_device(
    device_id: UUID,
    session: AsyncSession = Depends(get_db_session),
    current_user: User = Depends(get_current_user),
):

    device_uc = DeviceUseCase(session)
    result = await device_uc.delete_device(device_id, current_user)

    return result
