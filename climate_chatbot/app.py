import streamlit as st
from PIL import Image

from frontend.chat import (
    write_responses,
    manage_chat_state,
    chat_component
)
from frontend.sidebar import sidebar
from frontend.static_components import LOGO


def main_page() -> None:
    """
    Define the UI for the main chatbot page
    :return:
    """

    # App title
    st.set_page_config(page_title="Perspicue Climate", page_icon=LOGO)
    st.image(LOGO, width=120)
    st.header("Perspicue Climate")

    sidebar()

    manage_chat_state()
    write_responses()
    chat_component()

main_page()
