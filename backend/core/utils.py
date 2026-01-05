from fastapi import HTTPException, Header

# খুব simple security – later Telegram auth check লাগাতে পারো

API_SECRET = "changeme"  # চাইলে env var থেকে নাও

def verify_api_key(x_api_key: str = Header(default=None)):
    if x_api_key != API_SECRET:
        raise HTTPException(status_code=401, detail="Invalid API key")
    return True
