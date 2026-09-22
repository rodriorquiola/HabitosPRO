import anthropic

from app.services.ai.base import MensajeChat, ProveedorIA


class ClaudeProvider(ProveedorIA):
    def __init__(self, api_key: str, model: str = "claude-opus-5"):
        self._client = anthropic.AsyncAnthropic(api_key=api_key)
        self._model = model

    async def generar_respuesta(
        self,
        system_prompt: str,
        historial: list[MensajeChat],
        mensaje_usuario: str,
    ) -> str:
        messages = [{"role": m.rol, "content": m.contenido} for m in historial]
        messages.append({"role": "user", "content": mensaje_usuario})

        response = await self._client.messages.create(
            model=self._model,
            max_tokens=2048,
            system=system_prompt,
            messages=messages,
            output_config={"effort": "medium"},
        )

        return next((block.text for block in response.content if block.type == "text"), "")
