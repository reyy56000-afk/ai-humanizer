from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from humanizer import humanize_text

app = FastAPI()

# Folder where index.html is stored
templates = Jinja2Templates(directory="templates")


# Request model
class TextRequest(BaseModel):
    text: str


# Home Page
@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse(
        "index.html",
        {
            "request": request
        }
    )


# Humanizer API
@app.post("/humanize")
async def humanize(request: TextRequest):

    result = humanize_text(request.text)

    return {
        "success": True,
        "original": request.text,
        "humanized": result
    }


# Health Check
@app.get("/health")
async def health():
    return {
        "status": "running",
        "service": "AI Humanizer"
    }