import uuid

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models import Mensaje, RolMensaje, Usuario
from app.services.ai.base import MensajeChat
from app.services.ai.factory import obtener_proveedor_ia
from app.services.ai.prompts import SYSTEM_PROMPT

HISTORIAL_MAXIMO = 20

_ROL_A_CHAT = {RolMensaje.USUARIO: "user", RolMensaje.ASISTENTE: "assistant"}


async def procesar_mensaje_entrante(db: AsyncSession, telefono: str, texto: str) -> str:
    usuario = await _obtener_o_crear_usuario(db, telefono)
    historial = await _cargar_historial(db, usuario.id)

    proveedor = obtener_proveedor_ia()
    respuesta = await proveedor.generar_respuesta(
        system_prompt=SYSTEM_PROMPT,
        historial=historial,
        mensaje_usuario=texto,
    )

    db.add(Mensaje(usuario_id=usuario.id, rol=RolMensaje.USUARIO, contenido=texto))
    db.add(Mensaje(usuario_id=usuario.id, rol=RolMensaje.ASISTENTE, contenido=respuesta))
    await db.commit()

    return respuesta


async def _obtener_o_crear_usuario(db: AsyncSession, telefono: str) -> Usuario:
    result = await db.execute(select(Usuario).where(Usuario.telefono_whatsapp == telefono))
    usuario = result.scalar_one_or_none()
    if usuario is None:
        usuario = Usuario(telefono_whatsapp=telefono)
        db.add(usuario)
        await db.flush()
    return usuario


async def _cargar_historial(db: AsyncSession, usuario_id: uuid.UUID) -> list[MensajeChat]:
    result = await db.execute(
        select(Mensaje)
        .where(Mensaje.usuario_id == usuario_id)
        .order_by(Mensaje.fecha.desc())
        .limit(HISTORIAL_MAXIMO)
    )
    mensajes = list(reversed(result.scalars().all()))
    return [MensajeChat(rol=_ROL_A_CHAT[m.rol], contenido=m.contenido) for m in mensajes]
