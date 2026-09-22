import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Usuario(Base):
    """Un usuario = un número de WhatsApp. Alta implícita en el primer mensaje."""

    __tablename__ = "usuarios"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    telefono_whatsapp: Mapped[str] = mapped_column(String(20), unique=True, nullable=False, index=True)
    nombre: Mapped[str | None] = mapped_column(String(100), nullable=True)
    fecha_creacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )

    perfil: Mapped["Perfil | None"] = relationship(
        back_populates="usuario", uselist=False, cascade="all, delete-orphan"
    )
    objetivos: Mapped[list["Objetivo"]] = relationship(back_populates="usuario", cascade="all, delete-orphan")
    mensajes: Mapped[list["Mensaje"]] = relationship(back_populates="usuario", cascade="all, delete-orphan")
