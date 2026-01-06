from fastapi import FastAPI, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles

from backend.admin_panel.auth import verify_admin
from backend.admin_panel import db_admin

app = FastAPI()

templates = Jinja2Templates(directory="backend/admin_panel/templates")
app.mount("/admin/static", StaticFiles(directory="backend/admin_panel/static"), name="admin_static")

# ---------- Auth ----------
@app.get("/admin", response_class=HTMLResponse)
async def login_page(request: Request):
    return templates.TemplateResponse("login.html", {"request": request})

@app.post("/admin/login")
async def login(request: Request,
                username: str = Form(...),
                password: str = Form(...)):
    # Simple fixed login (পরে env var থেকে নিতে পারো)
    if username == "admin" and password == "1234":
        response = RedirectResponse("/admin/dashboard", status_code=302)
        response.set_cookie("admin", "true")
        return response
    return templates.TemplateResponse(
        "login.html",
        {"request": request, "error": "Invalid username or password"},
    )

@app.get("/admin/logout")
async def logout():
    response = RedirectResponse("/admin", status_code=302)
    response.delete_cookie("admin")
    return response

# ---------- Dashboard ----------
@app.get("/admin/dashboard", response_class=HTMLResponse)
async def dashboard(request: Request, admin=Depends(verify_admin)):
    stats = db_admin.get_stats()
    return templates.TemplateResponse(
        "dashboard.html",
        {"request": request, "stats": stats},
    )

# ---------- Tasks ----------
@app.get("/admin/tasks", response_class=HTMLResponse)
async def tasks_page(request: Request, admin=Depends(verify_admin)):
    tasks = db_admin.list_tasks()
    return templates.TemplateResponse(
        "tasks.html",
        {"request": request, "tasks": tasks},
    )

@app.post("/admin/tasks/add")
async def tasks_add(admin=Depends(verify_admin),
                    title: str = Form(...),
                    link: str = Form(...),
                    reward: float = Form(...)):
    db_admin.add_task(title, link, reward)
    return RedirectResponse("/admin/tasks", status_code=302)

@app.post("/admin/tasks/remove")
async def tasks_remove(admin=Depends(verify_admin),
                       task_id: int = Form(...)):
    db_admin.remove_task(task_id)
    return RedirectResponse("/admin/tasks", status_code=302)

@app.post("/admin/tasks/toggle")
async def tasks_toggle(admin=Depends(verify_admin),
                       task_id: int = Form(...),
                       active: int = Form(...)):
    db_admin.set_task_active(task_id, bool(active))
    return RedirectResponse("/admin/tasks", status_code=302)

# ---------- Channels ----------
@app.get("/admin/channels", response_class=HTMLResponse)
async def channels_page(request: Request, admin=Depends(verify_admin)):
    channels = db_admin.list_channels()
    return templates.TemplateResponse(
        "channels.html",
        {"request": request, "channels": channels},
    )

@app.post("/admin/channels/add")
async def channels_add(admin=Depends(verify_admin),
                       username: str = Form(...)):
    db_admin.add_channel(username)
    return RedirectResponse("/admin/channels", status_code=302)

@app.post("/admin/channels/remove")
async def channels_remove(admin=Depends(verify_admin),
                          channel_id: int = Form(...)):
    db_admin.remove_channel(channel_id)
    return RedirectResponse("/admin/channels", status_code=302)

# ---------- Users ----------
@app.get("/admin/users", response_class=HTMLResponse)
async def users_page(request: Request, admin=Depends(verify_admin)):
    users = db_admin.list_users()
    return templates.TemplateResponse(
        "users.html",
        {"request": request, "users": users},
    )

@app.post("/admin/users/ban")
async def users_ban(admin=Depends(verify_admin),
                    user_id: int = Form(...)):
    db_admin.set_user_ban(user_id, True)
    return RedirectResponse("/admin/users", status_code=302)

@app.post("/admin/users/unban")
async def users_unban(admin=Depends(verify_admin),
                      user_id: int = Form(...)):
    db_admin.set_user_ban(user_id, False)
    return RedirectResponse("/admin/users", status_code=302)

# ---------- Withdraws ----------
@app.get("/admin/withdraws", response_class=HTMLResponse)
async def withdraws_page(request: Request,
                         admin=Depends(verify_admin),
                         status: str = "pending"):
    withdraws = db_admin.list_withdraws(status=status)
    return templates.TemplateResponse(
        "withdraws.html",
        {"request": request, "withdraws": withdraws, "status": status},
    )

@app.post("/admin/withdraws/approve")
async def withdraws_approve(admin=Depends(verify_admin),
                            withdraw_id: int = Form(...)):
    db_admin.update_withdraw(withdraw_id, "approved")
    return RedirectResponse("/admin/withdraws?status=pending", status_code=302)

@app.post("/admin/withdraws/reject")
async def withdraws_reject(admin=Depends(verify_admin),
                           withdraw_id: int = Form(...)):
    db_admin.update_withdraw(withdraw_id, "rejected")
    return RedirectResponse("/admin/withdraws?status=pending", status_code=302)

# ---------- Logs ----------
@app.get("/admin/logs", response_class=HTMLResponse)
async def logs_page(request: Request, admin=Depends(verify_admin)):
    logs = db_admin.list_logs()
    return templates.TemplateResponse(
        "logs.html",
        {"request": request, "logs": logs},
    )
