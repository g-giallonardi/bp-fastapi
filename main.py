from fastapi import FastAPI
from api.v1.api_v1 import api_router
from middlewares.auth_middleware import JWTAuthMiddleware

app = FastAPI(title="BP FastAPI")

# Ajouter le middleware JWT
app.add_middleware(JWTAuthMiddleware)

# Ajouter les routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "API is running"}