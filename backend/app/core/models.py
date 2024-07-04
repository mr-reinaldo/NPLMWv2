from datetime import datetime
from sqlalchemy.orm import Mapped, mapped_column, registry, relationship
from sqlalchemy import ForeignKey, func
from uuid import uuid4, UUID

table_registry = registry()


@table_registry.mapped_as_dataclass
class User:
    __tablename__ = "users"

    id: Mapped[UUID] = mapped_column(
        init=False, primary_key=True, default=uuid4
    )
    username: Mapped[str] = mapped_column(unique=True, nullable=False)
    email: Mapped[str] = mapped_column(unique=True, nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    is_active: Mapped[bool] = mapped_column(default=True)
    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    devices: Mapped[list["Device"]] = relationship(
        "Device",
        init=False,
        back_populates="user",
        lazy="joined",
        uselist=True,
        cascade="all, delete-orphan",
    )


@table_registry.mapped_as_dataclass
class Device:
    __tablename__ = "devices"

    id: Mapped[UUID] = mapped_column(
        init=False, primary_key=True, default=uuid4
    )

    ip_address: Mapped[str] = mapped_column(unique=True, nullable=False)
    hostname: Mapped[str] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(nullable=False)
    password: Mapped[str] = mapped_column(nullable=False)
    driver_name: Mapped[str] = mapped_column(nullable=False)
    device_type: Mapped[str] = mapped_column(nullable=False)
    port_number: Mapped[int] = mapped_column(nullable=False)
    description: Mapped[str] = mapped_column(nullable=True)

    user_id: Mapped[UUID] = mapped_column(
        ForeignKey("users.id"), nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now()
    )
    updated_at: Mapped[datetime] = mapped_column(
        init=False, server_default=func.now(), onupdate=func.now()
    )

    user: Mapped[User] = relationship(
        "User", init=False, back_populates="devices", lazy="joined"
    )
