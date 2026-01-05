from fastapi import APIRouter, Depends
from pydantic import BaseModel
from backend.core import database
from backend.core.utils import verify_api_key

router = APIRouter(prefix="/api/admin", tags=["admin"])

class TaskCreate(BaseModel):
    title: str
    link: str
    reward: float

@router.get("/stats")
def stats(authorized: bool = Depends(verify_api_key)):
    conn = database._conn()
    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM users")
    total_users = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM tasks")
    total_tasks = cur.fetchone()[0]

    cur.execute("SELECT COUNT(*) FROM withdrawals WHERE status = 'pending'")
    pending_withdraws = cur.fetchone()[0]

    conn.close()

    return {
        "total_users": total_users,
        "total_tasks": total_tasks,
        "pending_withdraws": pending_withdraws,
    }

@router.post("/tasks")
def add_task(task: TaskCreate, authorized: bool = Depends(verify_api_key)):
    conn = database._conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO tasks (title, link, reward, active) VALUES (?, ?, ?, 1)",
        (task.title, task.link, task.reward),
    )
    conn.commit()
    conn.close()
    return {"message": "Task created"}

@router.get("/withdraws")
def list_withdraws(status: str = "pending", authorized: bool = Depends(verify_api_key)):
    conn = database._conn()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, user_id, amount, currency, status, created_at "
        "FROM withdrawals WHERE status = ? ORDER BY id DESC",
        (status,),
    )
    rows = cur.fetchall()
    conn.close()

    withdraws = [
        {
            "id": r[0],
            "user_id": r[1],
            "amount": r[2],
            "currency": r[3],
            "status": r[4],
            "created_at": r[5],
        }
        for r in rows
    ]
    return {"withdraws": withdraws}
