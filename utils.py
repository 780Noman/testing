import os
import openai
import streamlit as st
from datetime import datetime
from langchain_openai import ChatOpenAI

def enable_chat_history(func):
    def wrapper(*args, **kwargs):
        if "messages" not in st.session_state:
            st.session_state["messages"] = [{"role": "assistant", "content": "How can I help you?"}]
        
        # Display the chat history
        for msg in st.session_state["messages"]:
            st.chat_message(msg["role"]).write(msg["content"])
        
        func(*args, **kwargs)

    return wrapper

def display_msg(msg, author):
    """Method to display message on the UI

    Args:
        msg (str): message to display
        author (str): author of the message - user/assistant
    """
    if "messages" not in st.session_state:
        st.session_state["messages"] = []
    
    st.session_state.messages.append({"role": author, "content": msg})
    st.chat_message(author).write(msg)

def configure_llm():
    openai_api_key = st.secrets['secrets']["OPENAI_API_KEY"]

    model = "gpt-4"  # Default model; adjust as necessary

    try:
        client = openai.Client(api_key=openai_api_key)
        available_models = [{"id": i.id, "created": datetime.fromtimestamp(i.created)} for i in client.models.list() if str(i.id).startswith("gpt")]
        available_models = sorted(available_models, key=lambda x: x["created"])
        available_models = [i["id"] for i in available_models]

        model = st.sidebar.selectbox(
            label="Model",
            options=available_models,
            key="SELECTED_OPENAI_MODEL"
        )
    except openai.AuthenticationError as e:
        st.error(e.body["message"])
        st.stop()
    except Exception as e:
        st.error("Something went wrong. Please try again later.")
        st.stop()

    llm = ChatOpenAI(model_name=model, temperature=0, streaming=True, api_key=openai_api_key,max_tokens=500)
    return llm

def sync_st_session():
    for k, v in st.session_state.items():
        st.session_state[k] = v
