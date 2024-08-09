from fastapi import FastAPI, Form

from typing import Optional

import chat

app = FastAPI()


@app.get("/create-session")
def create_session() -> str:

    return chat.create_session()


@app.post("/index")
def index(url: str = Form(default="")):

    return chat.index(url)


@app.post('/ask')
def ask(
    url: str = Form(default=""),
    query: str = Form(default=""),
    session_id: Optional[str] = Form(default="")
):

    return chat.ask(url, query, session_id)

