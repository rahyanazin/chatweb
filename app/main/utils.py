import streamlit as st

from main import settings


def update_page_style():

    with open(settings.APP_STYLE_FILEPATH, "r") as f:
        page_style = f.read()

    st.markdown(page_style, unsafe_allow_html=True)


def add_styled_text(text, tag, font_size, text_align):

    st.markdown(f"<{tag} style='font-size: {font_size}; text-align: {text_align};'>{text}</{tag}>", unsafe_allow_html=True)


def break_lines(n=1):
    for _ in range(n):
        st.text("")
