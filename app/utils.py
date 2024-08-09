import random

import streamlit as st

import chat


def initialize_states():

    if "chat_storage" not in st.session_state:

        st.session_state.chat_storage = dict()

    if "chat_history" not in st.session_state:

        st.session_state.chat_history = []


def get_random_value():

    return random.randint(0, 100)


def submit_url():

    st.session_state.url = st.session_state.widget

    st.session_state.widget = ''


def on_url_changed():

    url = st.session_state.url_input

    st.session_state.url = url

    st.session_state.chat_session_id = chat.generate_session_id()

    chat.index(url)

    st.session_state.chat_history = [
        {"role": "assistant", "content": f"The content of website '{url}' has been loaded. How can I help you?"},
    ]

    st.session_state.url_input = None


def on_clear():

    url = st.session_state.url

    st.session_state.chat_history = [
        {"role": "assistant", "content": f"The content of website '{url}' has been loaded. How can I help you?"},
    ]


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


def update_page_style():

    with open("./style.html", "r") as f:
        page_style = f.read()

    st.markdown(page_style, unsafe_allow_html=True)


def add_styled_text(text, tag, font_size, text_align):

    st.markdown(f"<{tag} style='font-size: {font_size}; text-align: {text_align};'>{text}</{tag}>", unsafe_allow_html=True)


def break_lines(n=1):
    for _ in range(n):
        st.text("")


def show_chat_history():

    chat_history = st.session_state.get("chat_history", [])

    with st.container(height=500, border=True):

        if len(chat_history) == 0:

            st.write("Enter a website URL to load its content and ask something about it.")

        else:

            for message in chat_history:

                with st.chat_message(message["role"]):

                    st.write(message["content"])


def ask(url, query):

    return chat.ask(
        url=url,
        query=query,
        session_id=st.session_state.chat_session_id,
        chat_storage=st.session_state.chat_storage,
    )
