import httpx

from app.config import settings


async def enviar_mensaje_texto(destinatario_wa_id: str, texto: str) -> None:
    url = (
        f"https://graph.facebook.com/{settings.whatsapp_api_version}"
        f"/{settings.whatsapp_phone_number_id}/messages"
    )
    headers = {"Authorization": f"Bearer {settings.whatsapp_access_token}"}
    payload = {
        "messaging_product": "whatsapp",
        "to": destinatario_wa_id,
        "type": "text",
        "text": {"body": texto},
    }

    async with httpx.AsyncClient(timeout=15.0) as client:
        response = await client.post(url, headers=headers, json=payload)
        response.raise_for_status()
