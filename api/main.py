from fastapi import FastAPI, Form

from typing import Optional

import uuid

app = FastAPI()


@app.get("/create-session")
def create_session() -> str:

    return uuid.uuid4().hex


@app.post("/index")
def index(url: str = Form(default="")):

    return url


@app.post('/ask')
def ask(
    url: str = Form(default=""),
    query: str = Form(default=""),
    session_id: Optional[str] = Form(default="")
):
    return f"answer for question '{query}' about url '{url}' in session '{session_id}'"
