from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
import uvicorn

app = FastAPI()

# Sample data model
class Message(BaseModel):
    content: str
    sender: Optional[str] = "Anonymous"

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/api/v1/message")
async def read_message():
    return {"message": "Hello from backend!"}

@app.post("/api/v1/message")
async def send_message(msg: Message):
    return {"received": msg.content, "from": msg.sender}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
