import urllib3

import hashlib

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import settings

from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter

# from langchain_huggingface import HuggingFaceEmbeddings

import chromadb

# embeddings = HuggingFaceEmbeddings()


# https://python.langchain.com/v0.2/docs/integrations/chat/openai/

# https://python.langchain.com/v0.2/docs/integrations/text_embedding/openai/

# https://www.firecrawl.dev/pricing


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

    return


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


if __name__ == '__main__':
    url = "https://pt.wikipedia.org/wiki/Gabriel_Medina"

    index(url)

    index(url)

    index(url)

    url2 = "https://en.wikipedia.org/wiki/Brazil"

    index(url2)

    index(url2)

    pass
