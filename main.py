from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def HelloWorld():
    return { "message" : "Hello, world" }


@app.get('/health')
async def HealthStatus():
    return { "name" : "Task API", "version" : "1.0" , "endpoints" : ["/tasks"] }

