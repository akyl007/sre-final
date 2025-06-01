from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from prometheus_fastapi_instrumentator import Instrumentator
import uvicorn
import os

app = FastAPI()
Instrumentator().instrument(app).expose(app)
# Подключение папки со статикой
app.mount("/static", StaticFiles(directory="app/static"), name="static")

# Простой приветственный HTML на /
@app.get("/", response_class=HTMLResponse)
async def read_root():
    with open("app/static/index.html", "r", encoding="utf-8") as f:
        return f.read()

# Модель для POST
class Message(BaseModel):
    content: str
    sender: Optional[str] = "Anonymous"

# Исправлено: разрешён HEAD-запрос для мониторинга
@app.api_route("/health", methods=["GET", "HEAD"])
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
