# HábitoPRO

Chatbot de WhatsApp (con apps Android/iOS y web planificadas para etapas posteriores) que hace seguimiento de comidas y ejercicio, usando IA para gestionarlo en base a los objetivos del usuario. Personalidad amigable: mezcla de personal trainer, médico, nutricionista y deportista.

Ver `FITNESSPRO-objetivo.txt` para la declaración original del proyecto, y el roadmap por etapas para el plan completo.

## Stack (Etapa 0)

- Backend: Python 3.12 + FastAPI + SQLAlchemy async + PostgreSQL 15 + Alembic + Pydantic v2
- IA: capa de abstracción propia (`app/services/ai/`), proveedor inicial Claude (Anthropic)
- Infra: Docker Compose (local y como base del deploy en VPS)

## Levantar el proyecto localmente

```bash
cp .env.example .env
# completar ANTHROPIC_API_KEY en .env

docker compose up --build
```

- Backend: http://localhost:8100
- Health check: http://localhost:8100/health
- PostgreSQL: localhost:5440

## Migraciones (Alembic)

```bash
docker compose exec backend alembic revision --autogenerate -m "descripcion"
docker compose exec backend alembic upgrade head
```

## Estructura

```
backend/
  app/
    models/       # Usuario, Perfil, Objetivo, Mensaje (modelo de datos base, multi-tenant)
    services/ai/   # capa de abstracción de proveedor de IA (ProveedorIA, ClaudeProvider)
    routers/       # health, webhook de WhatsApp (Cloud API)
  alembic/
docker-compose.yml
```

## Próximos pasos (fuera del alcance de este repo por ahora)

- Alta y verificación de la cuenta de Meta WhatsApp Business Cloud API
- Deploy a VPS (Docker Compose + Nginx + SSL)
- Lógica de conversación completa del webhook de WhatsApp (Etapa 1)
