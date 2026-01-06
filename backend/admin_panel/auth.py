from fastapi import Request, HTTPException

def verify_admin(request: Request):
    if request.cookies.get("admin") != "true":
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True
