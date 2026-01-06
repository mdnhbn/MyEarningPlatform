from fastapi import FastAPI
from backend.core.database import init_db
from backend.api import user_api, admin_api, auth_api
from backend.admin_panel.main import app as admin_app

app = FastAPI()

# init DB on startup
@app.on_event("startup")
def startup_event():
    init_db()

# include APIs
app.include_router(user_api.router)
app.include_router(admin_api.router)
app.include_router(auth_api.router)

# mount admin panel under same app (using ASGI mount)
app.mount("", admin_app)
