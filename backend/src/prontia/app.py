from fastapi import FastAPI

from prontia.api import conversation

app = FastAPI()
app.include_router(conversation.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}
