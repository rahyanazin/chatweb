import uuid

import pickle

from pathlib import Path

from main import settings

from langchain_community.chat_message_histories import ChatMessageHistory


def serialize_object(obj, filepath):

    with open(filepath, 'wb') as f:
        pickle.dump(obj, f)


def deserialize_object(filepath):

    with open(filepath, 'rb') as f:
        return pickle.load(f)


def generate_session_id():

    return uuid.uuid4().hex


def create_session_history(session_id):

    Path(settings.CHAT_SESSION_DIRECTORY).mkdir(parents=True, exist_ok=True)

    serialize_object(
        ChatMessageHistory(),
        f"{settings.CHAT_SESSION_DIRECTORY}/{session_id}.pickle"
    )


def update_session_history(session_id, session_history):

    if session_id is None:
        return

    serialize_object(
        session_history,
        f"{settings.CHAT_SESSION_DIRECTORY}/{session_id}.pickle"
    )


def get_session_history(session_id):

    if session_id is None:
        return ChatMessageHistory()

    return deserialize_object(f"{settings.CHAT_SESSION_DIRECTORY}/{session_id}.pickle")


def create_session():

    session_id = generate_session_id()

    create_session_history(session_id)

    return session_id
