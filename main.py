from fastapi import FastAPI
from api.v1.api_v1 import api_router
from middlewares.auth_middleware import JWTAuthMiddleware
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="BP FastAPI")

app.add_middleware(JWTAuthMiddleware)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173"],
    allow_credentials=True, 
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["Content-Type", "Authorization"],
)

# Ajouter les routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"message": "API is running"}