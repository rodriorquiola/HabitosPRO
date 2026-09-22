from fastapi import FastAPI

from app.routers import health, whatsapp

app = FastAPI(title="HábitoPRO API")

app.include_router(health.router)
app.include_router(whatsapp.router)
