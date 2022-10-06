from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn

app = FastAPI()


@app.post('/webhook')
async def handle_webhook(data: dict):
    print(data)
    return {"Success": 200}

uvicorn.run(app, host="0.0.0.0", port=8000)
