import enum
import uuid
from datetime import date, datetime, timezone

from sqlalchemy import Boolean, Date, Enum, ForeignKey, Numeric, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.models.base import Base


class TipoObjetivo(str, enum.Enum):
    BAJAR_PESO = "bajar_peso"
    GANAR_MUSCULO = "ganar_musculo"
    RENDIMIENTO_DEPORTIVO = "rendimiento_deportivo"
    SALUD_GENERAL = "salud_general"


class Objetivo(Base):
    __tablename__ = "objetivos"

    id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    usuario_id: Mapped[uuid.UUID] = mapped_column(UUID(as_uuid=True), ForeignKey("usuarios.id"), nullable=False)

    tipo: Mapped[TipoObjetivo] = mapped_column(Enum(TipoObjetivo, name="tipo_objetivo_enum"), nullable=False)
    peso_objetivo_kg: Mapped[float | None] = mapped_column(Numeric(5, 2), nullable=True)
    fecha_inicio: Mapped[date] = mapped_column(Date, default=lambda: datetime.now(timezone.utc).date())
    fecha_objetivo: Mapped[date | None] = mapped_column(Date, nullable=True)
    activo: Mapped[bool] = mapped_column(Boolean, default=True)
    notas: Mapped[str | None] = mapped_column(Text, nullable=True)

    usuario: Mapped["Usuario"] = relationship(back_populates="objetivos")
