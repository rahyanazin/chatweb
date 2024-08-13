from fastapi import FastAPI, Form

from typing import Optional

from main import chat

from main import storage_chat_session

from main import storage_websites_content


app = FastAPI(title="Talk to your website API", swagger_ui_parameters={"defaultModelsExpandDepth": -1})


@app.post("/create-session", tags=["chat"])
def create_session() -> str:

    return storage_chat_session.create_session()


@app.post("/index", tags=["chat"])
def index(url: str = Form(default=None)):

    return storage_websites_content.index(url)


@app.post('/ask', tags=["chat"])
def ask(
    url: str = Form(default=None),
    query: str = Form(default=None),
    session_id: Optional[str] = Form(default=None)
):

    return chat.ask(url, query, session_id)
