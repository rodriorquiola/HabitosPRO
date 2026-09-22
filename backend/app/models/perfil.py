import enum
import uuid
from datetime import datetime, timezone

from sqlalchemy import DateTime, Enum, ForeignKey, Integer, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class Sexo(str, enum.Enum):
    MASCULINO = "masculino"
    FEMENINO = "femenino"
    OTRO = "otro"


class Perfil(Base):
    __tablename__ = "perfiles"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), ForeignKey("usuarios.id"), unique=True, nullable=False
    )

    edad: Mapped[int | None] = mapped_column(Integer, nullable=True)
    peso_kg: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    altura_cm: Mapped[int | None] = mapped_column(Integer, nullable=True)
    sexo: Mapped[Sexo | None] = mapped_column(Enum(Sexo, name="sexo_enum"), nullable=True)
    condiciones_medicas: Mapped[str | None] = mapped_column(Text, nullable=True)
    fecha_actualizacion: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    usuario: Mapped["Usuario"] = relationship(back_populates="perfil")
