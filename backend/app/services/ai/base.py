from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class MensajeChat:
    rol: str  # "user" | "assistant"
    contenido: str


class ProveedorIA(ABC):
    """Interfaz común para proveedores de IA conversacional.

    Cualquier proveedor nuevo (para sumar capacidad de visión, o para
    cambiar de modelo/vendor) se conecta implementando esta interfaz,
    sin tocar el código que la consume (routers/services de WhatsApp).
    """

    @abstractmethod
    async def generar_respuesta(
        self,
        system_prompt: str,
        historial: list[MensajeChat],
        mensaje_usuario: str,
    ) -> str: ...
