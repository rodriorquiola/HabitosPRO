from functools import lru_cache

from app.config import settings
from app.services.ai.base import ProveedorIA
from app.services.ai.claude_provider import ClaudeProvider


@lru_cache
def obtener_proveedor_ia() -> ProveedorIA:
    if settings.ai_provider == "claude":
        return ClaudeProvider(api_key=settings.anthropic_api_key, model=settings.claude_model)

    raise ValueError(f"Proveedor de IA no soportado: {settings.ai_provider}")
