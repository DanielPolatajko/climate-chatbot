import streamlit as st
from climate_chatbot.chatbot import answer


def manage_chat_state():
    """
    Store chatbot responses in the session state for
    an interactive chat experience with memory
    :return:
    """
    if "messages" not in st.session_state.keys():
        st.session_state.messages = [
            {"role": "assistant", "content": "How may I help you?"}
        ]


def write_responses() -> None:
    """
    Write out chatbot responses to the page
    :return:
    """
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.write(message["content"])


def generate_response(prompt_input: str) -> str:
    """
    Query the chatbot LLM backend for a response
    :param prompt_input: The prompt to provide the chatbot
    :return:
    """
    return answer(prompt_input)


def chat_component() -> None:
    """
    Define a chat box for the user to input questions
    and receive responses from the chatbot
    :return:
    """

    if prompt := st.chat_input(placeholder="What sections are required for a TCFD report?"):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.write(prompt)

    # Generate a new response if last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_response(prompt)
                st.write(response)
        message = {"role": "assistant", "content": response}
        st.session_state.messages.append(message)