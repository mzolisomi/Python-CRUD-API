from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

tasks = [
    {
        "id" : 0,
        "title" : "initialise the web framework",
        "done" : True
    },
    {
        "id" : 1,
        "title" : "Specify the port number for future purposes like when you want to tell the frontend to send requests to a backend, it needs to know the port the backend uses.",
        "done" : True
    },
    {
        "id" : 2,
        "title" : "Create the endpoints",
        "done" : True
    }
]

@app.get("/")
async def HelloWorld():
    return { "message" : "Hello, world" }


@app.get('/health')
async def HealthStatus():
    return { "name" : "Task API", "version" : "1.0" , "endpoints" : ["/tasks"] }

@app.get('/tasks')
async def Tasks():
    return tasks

@app.get('/tasks/{task_id}')
async def GetTask(task_id: int):
    for task in tasks:
        if task["id"] == task_id:
            return task
    return JSONResponse(
        status_code=404,
        content={"error": f"Task {task_id} not found"}
    )