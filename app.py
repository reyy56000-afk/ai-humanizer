from fastapi import FastAPI
from pydantic import BaseModel

from humanizer import humanize_text

app = FastAPI()


class TextRequest(BaseModel):
    text: str


@app.get("/")
def home():
    return {"message": "AI Humanizer API is running!"}


@app.post("/humanize")
def humanize(request: TextRequest):
    result = humanize_text(request.text)

    return {
        "original": request.text,
        "humanized": result
    }