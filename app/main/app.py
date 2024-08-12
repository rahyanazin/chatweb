
import streamlit as st

from main import chat


def initialize_states():

    if "chat_storage" not in st.session_state:

        st.session_state.chat_storage = dict()

    if "chat_history" not in st.session_state:

        st.session_state.chat_history = []


def on_url_changed():

    url = st.session_state.url_input

    st.session_state.url = url

    st.session_state.chat_session_id = chat.create_session()

    chat.index(url)

    st.session_state.chat_history = [
        {"role": "assistant", "content": f"The content of website '{url}' has been loaded. How can I help you?"},
    ]

    st.session_state.url_input = None


def url_input():

    url = st.text_input(
        key="url_input",
        value=None,
        label="Website URL",
        placeholder="Enter the URL of the website you want to chat with",
        label_visibility="collapsed",
        on_change=on_url_changed,
    )

    return url


def on_clear():

    url = st.session_state.url

    st.session_state.chat_history = [
        {"role": "assistant", "content": f"The content of website '{url}' has been loaded. How can I help you?"},
    ]


def on_question_asked(query):

    st.session_state.chat_history.append({"role": "user", "content": query})

    answer = chat.ask(st.session_state.url, query, st.session_state.chat_session_id)

    st.session_state.chat_history.append({"role": "assistant", "content": answer})


def show_chat_history():

    chat_history = st.session_state.get("chat_history", [])

    with st.container(height=500, border=True):

        if len(chat_history) == 0:

            st.write("Enter a website URL to load its content and ask something about it.")

        else:

            for message in chat_history:

                with st.chat_message(message["role"]):

                    st.write(message["content"])
