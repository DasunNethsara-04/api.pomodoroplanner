from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app: FastAPI = FastAPI()
app.add_middleware(CORSMiddleware,
                   allow_origins=['*'],
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"],
                   )

@app.get("/")
async def index()->dict[str, str]:
    return {"message":"Hello World"}