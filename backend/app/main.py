from fastapi import FastAPI

from app.core.settings import settings

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}
