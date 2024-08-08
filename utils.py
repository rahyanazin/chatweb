import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

import bs4

from langchain_chroma import Chroma
from langchain_community.document_loaders import WebBaseLoader
from langchain_openai import OpenAIEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


def get_vectorstore(url):

    loader = WebBaseLoader(
        web_paths=(url,),
        bs_kwargs=dict(
            parse_only=bs4.SoupStrainer(
                class_=("post-content", "post-title", "post-header")
            )
        ),
        requests_kwargs={"verify": False},
    )
    docs = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)

    splits = text_splitter.split_documents(docs)

    vectorstore = Chroma.from_documents(
        documents=splits,
        # embedding=OpenAIEmbeddings(http_client=httpx.Client(verify=False)),
        embedding=OpenAIEmbeddings()
        # client_settings=ChromaSettings(chroma_server_ssl_verify=False),
    )

    return vectorstore