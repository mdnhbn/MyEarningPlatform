from fastapi import APIRouter

router = APIRouter(prefix="/api/auth", tags=["auth"])

@router.get("/ping")
def ping():
    return {"status": "ok"}
