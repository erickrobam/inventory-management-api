from fastapi import FastAPI
from app.api.routes import router

app = FastAPI(title="Inventory Management API", version="1.0.0")
app.include_router(router, prefix="/api/v1")

@app.get("/health", tags=["operations"])
def health() -> dict[str, str]:
    return {"status": "ok"}
