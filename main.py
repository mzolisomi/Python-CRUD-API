from pydantic import BaseModel, Field, EmailStr
from fastapi import FastAPI, Response, Depends, HTTPException, Header
from fastapi.responses import JSONResponse
from typing import Optional
from database import get_db
from sqlalchemy.orm import Session
from models import Task
from typing import Any
import os 
from dotenv import load_dotenv
from supabase import create_client, AuthApiError
import httpx

load_dotenv()

SUPABASE_URL: str = os.environ["SUPABASE_URL"]
SUPABASE_KEY: str = os.environ["SUPABASE_KEY"]

print(repr(SUPABASE_URL))

app = FastAPI()
supabase = create_client(SUPABASE_URL, SUPABASE_KEY)

class NewUser(BaseModel):
    email: EmailStr = Field(..., description="Valid email address")
    password:str = Field(..., min_length=8, description="Password with minimun of 8 characters")

class TaskCreate(BaseModel):
    title : Optional[str] = None


class TaskUpdate(BaseModel):
    title : Optional[str] = None
    done : Optional[bool] = None

@app.get("/")
async def HelloWorld():
    return { "message" : "Hello, world" }

@app.get("/public/info")
async def HelloStranger():
    return JSONResponse(
        status_code=200,
        content={ "message" : "Hello Stranger! This info is public." }
    )
    

@app.get("/protected/profile")
async def GetProfile(authorization: Optional[str] = Header(default=None)):
    if not authorization or not authorization.startswith("Bearer "):
        return JSONResponse(
            status_code=401,
            content={"error": "Access token required"}
        )

    access_token = authorization.removeprefix("Bearer ").strip()

    if not access_token:
        return JSONResponse(
            status_code=401,
            content={"error": "Access token required"}
        )


    return JSONResponse(
        status_code=200,
        content={"message" : "You are logged in" }
    )

@app.post("/auth/signup", status_code=201)
async def Register(req: NewUser, db: Session = Depends(get_db)):
    if not req.email.strip() or not req.password.strip():
        return JSONResponse(status_code=400, content={"error": "Email and password are required"})

    try:
        response = supabase.auth.sign_up(
            {
                "email": req.email,
                "password": req.password
            }
        )
    except AuthApiError as e:
        message_text: str = (e.message or "").lower()

        if (
            e.status == 409
            or e.code == "user_already_exists"
            or "already registered" in message_text
            or "already exists" in message_text
        ):
            return JSONResponse(
                status_code=409,
                content={"error": "An account with this email already exists"}
            )

        return JSONResponse(
            status_code=e.status or 400,
            content={"error": e.message}
        )
    except httpx.RequestError:
        return JSONResponse(
            status_code=503,
            content={"error": "Could not reach the authentication service"}
        )

    if response.user is None:
        raise HTTPException(status_code=500, detail="Auth response did not include a user")

    user_data = response.user.model_dump(mode="json")  
    return JSONResponse(
        status_code=201,
        content={
            "user": user_data,
            "message" : "User registered successfully"
        }
    )

@app.post("/auth/login", status_code=200)
async def Login(req: NewUser, db: Session = Depends(get_db)):
    try:
        response = supabase.auth.sign_in_with_password(
            {
                "email": req.email,
                "password": req.password
            }
        )

        if response.user is None:
            return JSONResponse(
                status_code=401,
                content={ "error" : "Invalid email or password" }
            )
        user_data = response.user.model_dump(mode="json")
        return JSONResponse(
            status_code=200,
            content={
                "user": user_data,
                "message" : "User logged in successfully"
            }
        )
    except AuthApiError:
        return JSONResponse(
            status_code=401,
            content={"error" : "Invalid Credentials"}
        )


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


