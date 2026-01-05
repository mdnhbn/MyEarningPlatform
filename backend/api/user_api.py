from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from backend.core import database
from backend.core.utils import verify_api_key

router = APIRouter(prefix="/api/user", tags=["user"])

class WithdrawRequest(BaseModel):
    user_id: int        # Telegram ID
    amount: float
    currency: str

@router.get("/balance")
def get_balance(user_id: int, authorized: bool = Depends(verify_api_key)):
    bal = database.get_balance(user_id)
    return {"user_id": user_id, "balance": bal}

@router.get("/tasks")
def list_tasks(user_id: int, authorized: bool = Depends(verify_api_key)):
    conn = database._conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, title, link, reward, active FROM tasks WHERE active = 1 ORDER BY id DESC"
    )
    rows = cur.fetchall()
    conn.close()

    tasks = [
        {
            "id": r[0],
            "title": r[1],
            "link": r[2],
            "reward": r[3],
            "active": bool(r[4]),
        }
        for r in rows
    ]
    return {"tasks": tasks}

@router.post("/withdraw")
def create_withdraw(req: WithdrawRequest, authorized: bool = Depends(verify_api_key)):
    # check balance
    balance = database.get_balance(req.user_id)
    if req.amount > balance:
        raise HTTPException(status_code=400, detail="Insufficient balance")

    conn = database._conn()
    cur = conn.cursor()

    cur.execute("SELECT id FROM users WHERE telegram_id = ?", (req.user_id,))
    row = cur.fetchone()
    if not row:
        # auto create user
        u = database.get_or_create_user(req.user_id)
        user_db_id = u[0]
    else:
        user_db_id = row[0]

    cur.execute(
        "INSERT INTO withdrawals (user_id, amount, currency, status) VALUES (?, ?, ?, 'pending')",
        (user_db_id, req.amount, req.currency.upper()),
    )
    conn.commit()
    conn.close()

    database.update_balance(req.user_id, -req.amount)
    database.log_event("withdraw_request", f"user {req.user_id} requested {req.amount} {req.currency}")
    return {"message": "Withdraw request created", "status": "pending"}

@router.get("/profile")
def profile(user_id: int, authorized: bool = Depends(verify_api_key)):
    conn = database._conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, telegram_id, balance, banned, created_at FROM users WHERE telegram_id = ?",
        (user_id,),
    )
    row = cur.fetchone()
    conn.close()

    if not row:
        u = database.get_or_create_user(user_id)
        row = u

    return {
        "db_id": row[0],
        "telegram_id": row[1],
        "balance": row[2],
        "banned": bool(row[3]),
        "created_at": row[4],
        "total_earned": row[2],  # simple: assume balance == earned (later আলাদা field করতে পারো)
    }
