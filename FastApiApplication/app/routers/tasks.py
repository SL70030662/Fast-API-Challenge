from fastapi import APIRouter, HTTPException, status
from app.services.task_manager import task_manager

router = APIRouter()

@router.get("/tasks")
async def list_tasks():
    tasks = task_manager.list_tasks()
    return {"tasks": tasks}

@router.post("/tasks/cancel")
async def cancel_task(task_id: str):
    result = task_manager.cancel_task(task_id)
    if not result:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Task not found")
    return {"message": "Task cancelled successfully"}
