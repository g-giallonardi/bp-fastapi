from fastapi import APIRouter

router = APIRouter()

@router.get("/hello", tags=["example"])
async def hello():
    return {"message": "Hello, endpoint example !"}