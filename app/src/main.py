from fastapi import Depends, FastAPI, HTTPException, status
from sqlalchemy.orm import Session

from src.database import Base, engine, get_db
from src.models import Task
from src.schemas import TaskCreate, TaskResponse, TaskUpdate


Base.metadata.create_all(bind=engine)


app = FastAPI(
    title="TaskFlow API",
    version="1.0.0"
)


@app.get("/")
def root():
    return {
        "message": "TaskFlow API"
    }


@app.post(
    "/tasks",
    response_model=TaskResponse,
    status_code=status.HTTP_201_CREATED
)
def create_task(
    task: TaskCreate,
    db: Session = Depends(get_db)
):
    new_task = Task(
        title=task.title,
        description=task.description
    )

    db.add(new_task)
    db.commit()
    db.refresh(new_task)

    return new_task

@app.get(
    "/tasks",
    response_model=list[TaskResponse]
)
def list_tasks(
    db: Session = Depends(get_db)
):
    tasks = db.query(Task).all()

    return tasks


@app.get(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def get_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    return task

@app.put(
    "/tasks/{task_id}",
    response_model=TaskResponse
)
def update_task(
    task_id: int,
    task_update: TaskUpdate,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    task.title = task_update.title
    task.description = task_update.description
    task.completed = task_update.completed

    db.commit()
    db.refresh(task)

    return task

@app.delete(
    "/tasks/{task_id}",
    status_code=status.HTTP_204_NO_CONTENT
)
def delete_task(
    task_id: int,
    db: Session = Depends(get_db)
):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Task not found"
        )

    db.delete(task)
    db.commit()


@app.get("/health")
def health():
    return {
        "status": "healthy"
    }