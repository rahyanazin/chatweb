import hashlib

from main import settings

from langchain_chroma import Chroma

from langchain_community.document_loaders import WebBaseLoader

from langchain_openai import OpenAIEmbeddings

from langchain_text_splitters import RecursiveCharacterTextSplitter

import chromadb


def get_chroma_client():

    return chromadb.PersistentClient(path=settings.VECTORSTORE_PERSISTENT_DIRECTORY)


def get_collection_name(url):

    return hashlib.md5(url.encode()).hexdigest()


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


def index(url):

    if is_url_indexed(url):
        return

    url_collection_name = get_collection_name(url)

    loader = WebBaseLoader(web_paths=[url])

    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    splits = text_splitter.split_documents(docs)

    Chroma.from_documents(
        collection_name=url_collection_name,
        documents=splits,
        embedding=OpenAIEmbeddings(),
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
    # url_collection = get_collection(url)
    # assert sorted(url_collection.get()["ids"]) == sorted(vectordb.get()["ids"])

    return vectordb
