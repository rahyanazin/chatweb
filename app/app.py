import streamlit as st

from main import utils

from main.app import (
    initialize_states,
    url_input,
    on_clear,
    show_chat_history,
    on_question_asked
)


st.set_page_config(page_title="Talk to your website", page_icon="💬", layout="wide")


utils.update_page_style()


initialize_states()


utils.add_styled_text(text="Talk to your website", tag="h1", font_size="30px", text_align="center")


utils.break_lines(2)


url_input()


utils.break_lines(2)


if query := st.chat_input("Ask something"):

    on_question_asked(query)


show_chat_history()


st.button("Clear", on_click=on_clear)
