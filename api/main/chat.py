from langchain_openai import ChatOpenAI

from langchain.chains import create_history_aware_retriever, create_retrieval_chain

from langchain.chains.combine_documents import create_stuff_documents_chain

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

from langchain_core.runnables.history import RunnableWithMessageHistory

from main.storage_websites_content import index, get_url_vector_store

from main.storage_chat_session import get_session_history, update_session_history


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

    conversational_rag_chain = RunnableWithMessageHistory(
        rag_chain,
        lambda session_id: chat_storage,
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
