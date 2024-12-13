from fastapi import FastAPI

app: FastAPI = FastAPI()

@app.get("/")
async def index()->dict[str, str]:
    return {"message":"Hello World"}