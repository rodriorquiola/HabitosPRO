from fastapi import APIRouter, HTTPException, Query, Request
from fastapi.responses import PlainTextResponse

from app.config import settings

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
async def recibir_mensaje(request: Request):
    """Recibe mensajes entrantes de WhatsApp Cloud API.

    La lógica de conversación (resolver/crear Usuario, llamar al
    ProveedorIA, responder vía Cloud API) se conecta en la Etapa 1.
    """
    payload = await request.json()
    return {"status": "received"}
