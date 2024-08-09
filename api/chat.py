import urllib3

import hashlib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import settings

import pickle

from langchain_openai import ChatOpenAI
from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

from langchain.chains import create_history_aware_retriever, create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_community.chat_message_histories import ChatMessageHistory
from langchain_core.chat_history import BaseChatMessageHistory
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables.history import RunnableWithMessageHistory

# from langchain_huggingface import HuggingFaceEmbeddings

import chromadb

import uuid

# embeddings = HuggingFaceEmbeddings()

# https://python.langchain.com/v0.2/docs/integrations/chat/openai/

# https://python.langchain.com/v0.2/docs/integrations/text_embedding/openai/

# https://www.firecrawl.dev/pricing


def generate_session_id():

    return uuid.uuid4().hex


def create_session_history(session_id):

    from pathlib import Path

    Path.mkdir(Path(settings.CHAT_SESSION_DIRECTORY), exist_ok=True)

    with open(f"{settings.CHAT_SESSION_DIRECTORY}/{session_id}.pickle", 'wb') as f:
        pickle.dump(ChatMessageHistory(), f)


def create_session():

    session_id = generate_session_id()

    create_session_history(session_id)

    return session_id


def update_session_history(session_id, session_history):

    with open(f"{settings.CHAT_SESSION_DIRECTORY}/{session_id}.pickle", 'wb') as f:
        pickle.dump(session_history, f)


def get_session_history(session_id):

    with open(f"{settings.CHAT_SESSION_DIRECTORY}/{session_id}.pickle", 'rb') as f:
        return pickle.load(f)


def get_collection_name(url):

    return hashlib.md5(url.encode()).hexdigest()


def get_chroma_client():

    return chromadb.PersistentClient(path=settings.VECTORSTORE_PERSISTENT_DIRECTORY)


def get_collection(url):

    url_collection_name = get_collection_name(url)

    client = get_chroma_client()

    try:
        return client.get_collection(url_collection_name)

    except ValueError:
        return None


def is_url_indexed(url):

    collection = get_collection(url)

    return collection is not None


def delete_url_collection(url, client=None):

    url_collection_name = get_collection_name(url)

    client = get_chroma_client()

    client.delete_collection(url_collection_name)


def index(url):

    if is_url_indexed(url):
        # delete_url_collection(url)
        return

    url_collection_name = get_collection_name(url)

    loader = WebBaseLoader(web_paths=[url], verify_ssl=False)

    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    splits = text_splitter.split_documents(docs)

    Chroma.from_documents(
        collection_name=url_collection_name,
        documents=splits,
        embedding=OpenAIEmbeddings(),
        # embedding=OpenAIEmbeddings(http_client=httpx.Client(verify=False)),
        persist_directory=settings.VECTORSTORE_PERSISTENT_DIRECTORY
    )


def get_url_vector_store(url):

    url_collection_name = get_collection_name(url)

    vectordb = Chroma(
        collection_name=url_collection_name,
        persist_directory=settings.VECTORSTORE_PERSISTENT_DIRECTORY,
        embedding_function=OpenAIEmbeddings()
    )

    # I wasnt sure if I was getting exactly only the documents of the given collection name
    url_collection = get_collection(url)
    assert sorted(url_collection.get()["ids"]) == sorted(vectordb.get()["ids"])

    return vectordb


def get_rag_chain(url, chat_storage):

    index(url)

    vectorstore = get_url_vector_store(url)

    retriever = vectorstore.as_retriever()

    llm = ChatOpenAI(model="gpt-4o-mini")

    # Contextualize question #
    contextualize_q_system_prompt = (
        "Given a chat history and the latest user question "
        "which might reference context in the chat history, "
        "formulate a standalone question which can be understood "
        "without the chat history. Do NOT answer the question, "
        "just reformulate it if needed and otherwise return it as is."
    )

    contextualize_q_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", contextualize_q_system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    history_aware_retriever = create_history_aware_retriever(
        llm, retriever, contextualize_q_prompt
    )

    # Answer question #
    system_prompt = (
        "You are an assistant for question-answering tasks. "
        "Use the following pieces of retrieved context to answer "
        "the question. If you don't know the answer, say that you "
        "don't know. Use three sentences maximum and keep the "
        "answer concise."
        "\n\n"
        "{context}"
    )
    qa_prompt = ChatPromptTemplate.from_messages(
        [
            ("system", system_prompt),
            MessagesPlaceholder("chat_history"),
            ("human", "{input}"),
        ]
    )
    question_answer_chain = create_stuff_documents_chain(llm, qa_prompt)

    rag_chain = create_retrieval_chain(history_aware_retriever, question_answer_chain)

    # Statefully manage chat history #
    # def get_session_history(session_id: str) -> BaseChatMessageHistory:
    #     if session_id not in chat_storage:
    #         chat_storage[session_id] = ChatMessageHistory()
    #     return chat_storage[session_id]

    def get_session_history(session_id: str) -> BaseChatMessageHistory:
        return chat_storage

    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        get_session_history,
        input_messages_key="input",
        history_messages_key="chat_history",
        output_messages_key="answer",
    )

    return conversational_rag_chain


def ask(url, query, session_id):

    chat_storage = get_session_history(session_id)

    rag_chain = get_rag_chain(url, chat_storage)

    answer = rag_chain.invoke(
        {"input": query},
        config={
            "configurable": {"session_id": session_id}
        },
    )["answer"]

    update_session_history(session_id, chat_storage)

    # get_session_history(session_id)
    # len(get_session_history(session_id).messages)

    return answer


class ChatWebClient():

    def __init__(self, chat_storage=dict()):

        self.chat_storage = chat_storage

    def update(self, url):

        session_id = generate_session_id()

        index(url)

        return session_id

    def ask(self, url, query, session_id=None):

        answer = ask(url, query, session_id)

        return answer


if __name__ == '__main__':
    url = "https://pt.wikipedia.org/wiki/Gabriel_Medina"

    index(url)

    index(url)

    index(url)

    url2 = "https://en.wikipedia.org/wiki/Brazil"

    index(url2)

    index(url2)

    pass
