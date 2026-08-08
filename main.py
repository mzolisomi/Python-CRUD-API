from pydantic import BaseModel
from fastapi import FastAPI, Response, Depends
from fastapi.responses import JSONResponse
from typing import Optional
from database import get_db
from sqlalchemy.orm import Session
from models import Task
from typing import Any

app = FastAPI()


class TaskCreate(BaseModel):
    title : Optional[str] = None

class TaskUpdate(BaseModel):
    title : Optional[str] = None
    done : Optional[bool] = None

@app.get("/")
async def HelloWorld():
    return { "message" : "Hello, world" }


@app.get('/health')
async def HealthStatus() -> dict[str, Any]:
    return { "name" : "Task API", "version" : "1.0" , "endpoints" : ["/tasks"] }
# DONE
@app.get('/tasks')
async def Tasks(db: Session = Depends(get_db)):
    tasks = db.query(Task).all()
    return tasks

# DONE
@app.get('/tasks/{task_id}')
async def GetTask(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        return JSONResponse(
            status_code=404,
            content={"error": f"Task {task_id} not found"}
        )
    
    return task

# DONE
@app.post("/tasks")
async def AddTask(req: TaskCreate, db: Session = Depends(get_db)):
    if (req.title is None or req.title.strip() == ""):
        return JSONResponse(
            status_code=400,
            content={"error": "Title is required" }
        )

    new_task = Task(title=req.title.strip(), done=False)
    db.add(new_task)
    db.commit()
    db.refresh(new_task)
    return new_task

# DONE
@app.put("/tasks/{task_id}")
async def UpdateTask(task_id: int, req: TaskUpdate, db: Session = Depends(get_db)):
    if req.title is None and req.done is None:
        return JSONResponse(
            status_code = 400,
            content= { "error" : "Please update title or status of the task"}
        )

    if req.title is not None and req.title.strip() == "":
        return JSONResponse(
            status_code = 400,
            content={ "error" : "Please provide a title"}
        )

    task = db.query(Task).filter(Task.id == task_id).first()
    if task is None:
        return JSONResponse(
            status_code = 404,
            content = { "error" : f"No task with id '{task_id}'" }
        )
    if req.title is not None:
        task.title = req.title
    if req.done is not None:
        task.done = req.done

    db.commit()
    db.refresh(task)
    return task


# DONE
@app.delete("/tasks/{task_id}")
async def DeleteTask(task_id: int, db: Session = Depends(get_db)):
    task = db.query(Task).filter(Task.id == task_id).first()

    if task is not None:
        db.delete(task)
        db.commit()
        return Response(status_code = 204)
    return Response(
            status_code = 404
        )