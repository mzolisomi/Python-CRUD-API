from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def HelloWorld():
    return { "message" : "Hello, world" }

