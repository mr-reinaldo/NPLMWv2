from fastapi import HTTPException, Response
from http import HTTPStatus

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from uuid import UUID

from app.core.models import Device
from app.core.models import User

from app.schemas.device_schema import (
    DeviceSchema,
    DeviceSchemaPublic,
    DeviceSchemaUpdate,
    DeviceSchemaList,
)

from app.schemas.message_schema import MessageSchema


class DeviceUseCase:

    def __init__(self, session: AsyncSession):
        self._session = session

    async def create_device(
        self, device: DeviceSchema, current_user: User
    ) -> DeviceSchemaPublic:

        new_device = Device(
            ip_address=str(device.ip_address),
            hostname=device.hostname,
            username=device.username,
            password=device.password,
            driver_name=device.driver_name,
            device_type=device.device_type,
            port_number=device.port_number,
            description=device.description,
            user_id=current_user.id,
        )

        query = select(Device).filter(
            (Device.ip_address == new_device.ip_address)
            | (Device.hostname == new_device.hostname)
        )
        result = await self._session.execute(query)
        existing_device = result.scalars().first()

        if existing_device:
            if existing_device.ip_address == new_device.ip_address:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail="Já existe um dispositivo com esse endereço IP",
                )
            if existing_device.hostname == new_device.hostname:
                raise HTTPException(
                    status_code=HTTPStatus.BAD_REQUEST,
                    detail="Já existe um dispositivo com esse hostname",
                )

        self._session.add(new_device)
        await self._session.commit()
        await self._session.refresh(new_device)

        return MessageSchema(message="Dispositivo criado com sucesso")

    async def get_device(
        self, device_id: UUID, current_user: User
    ) -> DeviceSchemaPublic:
        query = select(Device).filter(
            Device.id == device_id, Device.user_id == current_user.id
        )
        result = await self._session.execute(query)
        device = result.scalars().first()

        if not device:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Dispositivo não encontrado",
            )

        return device

    async def list_devices(
        self, current_user: User, skip: int = 0, limit: int = 10
    ) -> DeviceSchemaList:
        query = (
            select(Device)
            .filter(Device.user_id == current_user.id)
            .offset(skip)
            .limit(limit)
        )
        result = await self._session.execute(query)
        devices_db = result.scalars().unique().all()

        if not devices_db:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Nenhum dispositivo encontrado",
            )

        return {"devices": devices_db}

    async def update_device(
        self, device_id: UUID, device: DeviceSchemaUpdate, current_user: User
    ) -> DeviceSchemaPublic:
        query = select(Device).filter(
            Device.id == device_id, Device.user_id == current_user.id
        )
        result = await self._session.execute(query)
        device_db = result.scalars().first()

        if not device_db:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Dispositivo não encontrado",
            )

        if device.ip_address:
            device_db.ip_address = str(device.ip_address)
        if device.hostname:
            device_db.hostname = device.hostname
        if device.username:
            device_db.username = device.username
        if device.password:
            device_db.password = device.password
        if device.driver_name:
            device_db.driver_name = device.driver_name
        if device.device_type:
            device_db.device_type = device.device_type
        if device.port_number:
            device_db.port_number = device.port_number
        if device.description:
            device_db.description = device.description

        await self._session.commit()
        await self._session.refresh(device_db)

        return MessageSchema(message="Dispositivo atualizado com sucesso")

    async def delete_device(self, device_id: UUID, current_user: User) -> Response:
        query = select(Device).filter(
            Device.id == device_id, Device.user_id == current_user.id
        )
        result = await self._session.execute(query)
        device_db = result.scalars().first()

        if not device_db:
            raise HTTPException(
                status_code=HTTPStatus.NOT_FOUND,
                detail="Dispositivo não encontrado",
            )

        await self._session.delete(device_db)
        await self._session.commit()

        return Response(status_code=HTTPStatus.NO_CONTENT)
