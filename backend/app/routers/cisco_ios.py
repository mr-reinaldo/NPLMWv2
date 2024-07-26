from fastapi import APIRouter, Depends
from http import HTTPStatus
from app.core.auth import get_current_user
from app.core.models import User

from app.schemas.netmiko_schemas import NetmikoConn
from app.schemas.message_schema import MessageSchema
from app.drivers.router_ios import RouterIOS

router = APIRouter(tags=["CISCO IOS"])


@router.post(
    "/cisco-ios/interfaces",
    status_code=HTTPStatus.CREATED,
)
async def get_interfaces(
    device: NetmikoConn,
    current_user: User = Depends(get_current_user),
):

    conn = RouterIOS(device)
    conn.connect()

    if conn._net_connect is None:
        return {"message": "Failed to connect to device."}

    interfaces = conn.get_interfaces()

    conn.disconnect()

    return interfaces
