from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from anthropic import Anthropic
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()
client = Anthropic()

app.mount("/static", StaticFiles(directory="templates"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse(request, "index.html")

class NotesInput(BaseModel):
    notes: str

@app.post("/generate")
async def generate(input: NotesInput):
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"Based on the following study notes, generate one clear question that tests deep understanding. Only return the question, nothing else. \n\nNotes: {input.notes}"
            }
        ]
    )
    return {"question": message.content[0].text}
