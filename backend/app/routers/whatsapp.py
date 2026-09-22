import logging

from fastapi import APIRouter, Depends, HTTPException, Query, Request
from fastapi.responses import PlainTextResponse
from sqlalchemy.ext.asyncio import AsyncSession

from app.config import settings
from app.database import get_db
from app.services.conversacion import procesar_mensaje_entrante
from app.services.whatsapp_client import enviar_mensaje_texto

logger = logging.getLogger(__name__)

router = APIRouter()


@router.get("/webhook/whatsapp")
async def verificar_webhook(
    hub_mode: str = Query(alias="hub.mode"),
    hub_verify_token: str = Query(alias="hub.verify_token"),
    hub_challenge: str = Query(alias="hub.challenge"),
):
    """Verificación del webhook exigida por Meta al configurar la Cloud API."""
    if hub_mode == "subscribe" and hub_verify_token == settings.whatsapp_verify_token:
        return PlainTextResponse(hub_challenge)
    raise HTTPException(status_code=403, detail="Token de verificación inválido")


@router.post("/webhook/whatsapp")
async def recibir_mensaje(request: Request, db: AsyncSession = Depends(get_db)):
    """Recibe mensajes entrantes de WhatsApp Cloud API y responde con el bot."""
    payload = await request.json()

    for entry in payload.get("entry", []):
        for change in entry.get("changes", []):
            valor = change.get("value", {})
            for mensaje in valor.get("messages", []):
                if mensaje.get("type") != "text":
                    continue

                telefono = mensaje["from"]
                texto = mensaje["text"]["body"]

                try:
                    respuesta = await procesar_mensaje_entrante(db, telefono, texto)
                    await enviar_mensaje_texto(telefono, respuesta)
                except Exception:
                    logger.exception("Error procesando mensaje de %s", telefono)

    return {"status": "received"}
