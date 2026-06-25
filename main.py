from fastapi import FastAPI, Request
from fastapi.responses import StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from anthropic import Anthropic
from dotenv import load_dotenv
import markdown
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
    def stream():
        with client.messages.stream(
            model="claude-sonnet-4-6",
            max_tokens=1024,
            messages=[
                {
                    "role": "user",
                    "content": f"Based on the following study notes, generate one clear question that tests deep understanding. Only return the question, nothing else. \n\nNotes: {input.notes}"
                }
            ]
        ) as stream: 
            for text in stream.text_stream:
                yield text
    return StreamingResponse(stream(), media_type="text/plain")

class FeedbackInput(BaseModel):
    question: str
    answer: str

@app.post("/feedback")
async def feedback(input: FeedbackInput):
    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"A student was asked the following question: {input.question}\n\nTheir answer was: {input.answer}\n\nEvaluate their answer. Tell them what they got right, what they got wrong, and how they could improve. Be concise and encourging."
            }
        ]
    )
    return {"feedback": markdown.markdown(message.content[0].text)}