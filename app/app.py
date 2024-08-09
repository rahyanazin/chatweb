import streamlit as st

from utils import (
    update_page_style,
    add_styled_text,
    break_lines,
    show_chat_history,
    url_input,
    initialize_states,
    ask,
    on_clear,
)

st.set_page_config(page_title="Talk to your website", page_icon="💬", layout="wide")

update_page_style()

initialize_states()

add_styled_text(text="Talk to your website", tag="h1", font_size="30px", text_align="center")

break_lines(2)

url_input()

break_lines(2)

if query := st.chat_input("Ask something"):

    st.session_state.chat_history.append({"role": "user", "content": query})

    answer = ask(st.session_state.url, query)

    st.session_state.chat_history.append({"role": "assistant", "content": answer})

show_chat_history()

st.button("Clear", on_click=on_clear)

# add_styled_text(text="✌", tag="footer", font_size="20px", text_align="right")
