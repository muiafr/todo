from http import HTTPStatus

from sqlalchemy import select

from fastapi import APIRouter, HTTPException

from db.db import Session
from models.models import TaskTable
from schemas.schemas import TaskRead, TaskCreate, TaskUpdate

router = APIRouter(tags=["tasks"], prefix="/tasks")

@router.get("/", response_model=list[TaskRead], status_code=201)
async def get_tasks(db: Session):
    result = await db.execute(select(TaskTable))
    tasks = result.scalars().all()
    return tasks

@router.get("/{task_id}" , response_model=TaskRead, status_code=200)
async def get_task(db: Session, task_id: int):
    result = await db.execute(select(TaskTable).where(TaskTable.id == task_id))
    task = result.scalar()
    if task is None:
        raise HTTPException(status_code=HTTPStatus.NOT_FOUND, detail="Task not found")
    return task

@router.post("/create", response_model=TaskRead, status_code=201)
async def create_task(db: Session, task: TaskCreate):
    new_task = TaskTable(
        title=task.title,
        description=task.description,
        status=task.status)

    db.add(new_task)

    try:
        await db.commit()
        await db.refresh(new_task)

    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

    return new_task

@router.delete("/{task_id}", response_model=TaskRead)
async def delete_task(db: Session, task_id: int):
    result = await db.execute(
        select(TaskTable).where(TaskTable.id == task_id)
    )

    task = result.scalar_one_or_none()

    if task is None:
        raise HTTPException(status_code=404, detail="Task not found")

    try:
        await db.delete(task)
        await db.commit()
    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )

    return task

@router.patch("/{task_id}", response_model=TaskRead, status_code=200)
async def update_task(db: Session, task_id: int, task: TaskUpdate):
    result = await db.execute(
        select(TaskTable).where(TaskTable.id == task_id)
    )

    existing_task = result.scalar_one_or_none()

    if existing_task is None:
        raise HTTPException(
            status_code=HTTPStatus.NOT_FOUND,
            detail="Task not found"
        )

    try:
        existing_task.title = task.title
        existing_task.description = task.description
        existing_task.status = task.status

        await db.commit()
        await db.refresh(existing_task)

    except Exception:
        await db.rollback()
        raise HTTPException(
            status_code=HTTPStatus.INTERNAL_SERVER_ERROR,
            detail="Internal server error"
        )

    return existing_task





